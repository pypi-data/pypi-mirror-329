# AUTOGENERATED! DO NOT EDIT! File to edit: ../notebooks/10_storage.ipynb.

# %% auto 0
__all__ = ['DATASTACK_EXT', 'L', 'Layers', 'raw_to_datastack', 'tree', 'underscorify', 'append', 'append_list', 'repack',
           'max_and_sum_spectra', 'make_raw_preview', 'parse_rpl', 'DataStack']

# %% ../notebooks/10_storage.ipynb 29
import maxrf4u

import numpy as np 
import dask 
import dask.array as da 
from dask.diagnostics import ProgressBar 
#import dask_ndfilters # obsolete 
from dask_image.ndfilters import gaussian_filter
import re 
import os 
import zarr 
from IPython.display import HTML 
import cv2
import matplotlib.pyplot as plt 
import scipy.signal as ssg 
import time 
import skimage as sk 
from pathlib import Path

# %% ../notebooks/10_storage.ipynb 30
# CONSTANTS 
DATASTACK_EXT = '.datastack' 


# COMPUTION ORDER 

class Layers: 
    
    def __init__(self): 
        
        self.LAYERS = ['MAXRF_CUBE', 
                       'MAXRF_MAXSPECTRUM', 
                       'MAXRF_SUMSPECTRUM', 
                       'MAXRF_ENERGIES', 
                       'HOTMAX_PIXELS', 
                       'HOTMAX_SPECTRA', 
                       'HOTMAX_BASELINES', 
                       'HOTMAX_NOISELINES', 
                       'MAPS_IMVIS'] 
        
        for l in self.LAYERS: 
            setattr(self, l, l.lower())

L = Layers()




# functions 

def raw_to_datastack(raw_file, rpl_file, output_dir=None, datapath=L.MAXRF_CUBE, verbose=True, 
                    flip_horizontal=False, flip_vertical=False): 
    '''Convert Bruker Macro XRF (.raw) data file *raw_filename* and (.rpl) shape file *rpl_filename*.  
    
    into a Zarr Zipstore datastack file (.datastack).
    ''' 

    print('Please wait while preparing data conversion...')
    
    # generate datastack file path from raw_file and output_dir   
    if output_dir is None: 
        # save in same folder 
        datastack_file = re.sub('\\.raw$', '', raw_file) + DATASTACK_EXT 
        
    else: 
        # save in output folder 
        assert os.path.exists(output_dir),  'Can not save to non-existing directory.'     
        basename = os.path.basename(raw_file) 
        basename = re.sub('\\.raw$', '', basename) + DATASTACK_EXT
        datastack_file = os.path.join(output_dir, basename)
        
    # read data cube shape and dtype from .rpl file 
    dtype, shape = parse_rpl(rpl_file, verbose=verbose)
    
    # create numpy memory map with proper orientation 
    v_stride = 1
    h_stride = 1
    if flip_vertical: 
        v_stride = -1
    if flip_horizontal:
        h_stride = -1 
    
    print('Creating memory map...')
    raw_mm = np.memmap(raw_file, dtype=dtype, mode='r', shape=shape)[::v_stride, ::h_stride] 

    # initializing dask array 
    arr = da.from_array(raw_mm) 
    arr = arr.astype(np.float32)
    
    # schedule spectral gaussian smoothing computation  
    smoothed = gaussian_filter(arr, (0, 0, 7)) 
    
    # create and open an empty zip file
    zs = zarr.ZipStore(datastack_file, mode='w') 
    
    if verbose: 
        print(f'Writing: {datastack_file}...')

    # compute and write maxrf data to zipstore 
    with ProgressBar(): 
        smoothed.to_zarr(zs, component=datapath) 
        
    zs.close()
    
    # compute sum and max spectra and append to zipstore 
    
    y_max, y_sum = max_and_sum_spectra(datastack_file, datapath=L.MAXRF_CUBE)
    
    append(y_max, L.MAXRF_MAXSPECTRUM, datastack_file)
    append(y_sum, L.MAXRF_SUMSPECTRUM, datastack_file)
    
    

def tree(datastack_file, show_arrays=False): 
    '''Prints content tree of *datastack_file* '''

    with zarr.ZipStore(datastack_file, mode='r') as zs: 
        root = zarr.group(store=zs) 
        tree = root.tree(expand=True).__repr__()
        print(f'{datastack_file}:\n\n{tree}')  
        
        if show_arrays:        
            datasets = sorted(root)
            arrays_html = ''

            for ds in datasets: 
                arr = da.from_array(root[ds])
                html = arr._repr_html_()
                arrays_html = f'{arrays_html}- Dataset: <h style="color:brown">{ds}</h>{html}' 
   
            return HTML(arrays_html)

def underscorify(datapath, datapath_list, extra_underscore=True): 
    '''Append extra underscore if *datapath* exists to prevent overwriting. 
    
    If *extra_underscore=False* return (latest) datapath with most underscores'''
    
    if datapath in datapath_list: 
        r = re.compile(f'{datapath}_*$')
        datapath = sorted(filter(r.match, datapath_list))[-1]
        
        if extra_underscore: 
            datapath = datapath + '_'
        
    return datapath 


def append(arr, datapath, datastack_file): 
    '''Add numpy or dask array *arr* to *datastack_file* in folder *datapath*.'''
    
    if not isinstance(arr, dask.array.Array):  
        arr = da.from_array(arr) 
            
    with zarr.ZipStore(datastack_file, mode='a') as zs: 
        root = zarr.group(store=zs)
        
        # append underscores to make unique if datapath exists 
        datapath_list = sorted(root) 
        datapath = underscorify(datapath, datapath_list)
        
        # write      
        arr.to_zarr(zs, component=datapath)

        
def append_list(ragged_list, datapath, datastack_file, nan=-9999): 
    '''Wrapper around append() to store iregular (ragged) lists of lists as regular padded arrays.  
    
    Currently only working for two dimensional lists of integers. Padding is done with nan=-9999. 
    ''' 
    
    padded_array = _straighten(ragged_list, nan=nan) 
        
    append(padded_array, datapath, datastack_file) 
    

def repack(datastack_file, select='all', overwrite=True, verbose=False): 
    '''Repack *datastack_file* by deleting and renaming all but latest datasets. 
    
    Automatic selection of latest datasets can be overriden be providing list of *select* datasets''' 
    
    if verbose: 
        tree(datastack_file)
    
    # open existing zipstore  
    zs = zarr.ZipStore(datastack_file, mode='r') 
    root = zarr.group(store=zs)
    datapath_list = sorted(root)  
    
    # select newest version (most underscores) for all datasets
    if select == 'all': 
        selected = sorted(set([underscorify(dp, datapath_list, extra_underscore=False) for dp in datapath_list])) 
    # select newest version (most underscores) for datasets in select
    else: 
        selected = sorted(set([underscorify(dp, datapath_list, extra_underscore=False) for dp in select]))       
    
    # remove underscores 
    renamed = [re.sub('_*$', '', s) for s in selected] 
    
    # create and open new empty zipstore 
    datastack_file_new = datastack_file + '_temp'
    zs_new = zarr.ZipStore(datastack_file_new, mode='w') 
    
    # copy selected datasets into new zipstore 
    with ProgressBar(): 
        for src, dst in zip(selected, renamed): 
            print(f'Repacking dataset: \'{src}\'') 
            arr = da.from_array(root[src])
            arr.to_zarr(zs_new, component=dst)
    
    zs.close()
    zs_new.close()
    
    # finally overwrite old with new  
    if overwrite: 
        os.replace(datastack_file_new, datastack_file)
    
    if verbose:
        print()
        tree(datastack_file)
        

def max_and_sum_spectra(datastack_file, datapath=L.MAXRF_CUBE): 
    '''Compute sum spectrum and max spectrum for 'maxrf' dataset in *datastack_file*. 
    
    Returns: *y_sum*, *y_max*'''
    
    # open existing zipstore  
    zs = zarr.ZipStore(datastack_file, mode='r') 
    root = zarr.group(store=zs)
    
    # initialize dask array 
    arr = da.from_array(root[datapath])
        
    # flatten (better avoid)
    h, w, d = arr.shape 
    #flat_shape = h * w, d
    #with dask.config.set(**{'array.slicing.split_large_chunks': True}):
    #    arr_flat = arr.reshape(flat_shape) #, limit='128 MiB') 
    #
    ## schedule computations 
    #sum_spectrum = arr_flat.sum(axis=0)
    #max_spectrum = arr_flat.max(axis=0)
    sum_spectrum = arr.sum(axis=(0, 1))
    max_spectrum = arr.max(axis=(0, 1))
    
    # compute 
    print('Computing max spectrum...')
    with ProgressBar():
        y_max = max_spectrum.compute() 
    print('Computing sum spectrum...')
    with ProgressBar(): 
        y_sum = sum_spectrum.compute() / (h * w)
        
    zs.close()
     
    return y_max, y_sum 


def make_raw_preview(raw_file, rpl_file, output_dir=None, show=False, save=True, verbose=False): 
    '''
    Create preview image of raw file to inspect scan orientation. 
    '''

    # read data cube shape and dtype from .rpl file
    dtype, shape = parse_rpl(rpl_file, verbose=verbose)
    
    # create numpy memory map 
    raw_mm = np.memmap(Path(raw_file), dtype=dtype, mode='r', shape=shape)  
    
    # create max-spectrum 
    raw_flat = raw_mm.reshape([-1, depth])
    raw_max = np.max(raw_flat, axis=0)
    
    # locate highest peak 
    max_peak_idx = np.argmax(raw_max)
    
    # integrate max peak slice 
    max_peak_map = np.average(raw_mm[:,:,max_peak_idx-10:max_peak_idx+10], axis=2)
    raw_preview = sk.exposure.equalize_hist(max_peak_map) 

    if output_dir is None: 
        # save in same folder 
        preview_file = raw_file + '_preview.png'
        
    else: 
        # save in output folder 
        assert os.path.exists(output_dir),  'Can not save to non-existing directory.'     
        basename = os.path.basename(raw_file) 
        basename = basename + '_preview.png'
        preview_file = os.path.join(output_dir, basename)

    if save: 
        print(f'Saving: {preview_file}...')
        plt.imsave(preview_file, raw_preview) 

    if show: 
        fig, ax = plt.subplots()
        ax.imshow(raw_preview)
        ax.set_title(preview_file)

    return raw_preview 

def parse_rpl(rpl_file, verbose=False): 
    '''Read .rpl shape file and return shape and dtype. '''

    # read data cube shape from .rpl file 
    with open(rpl_file, 'r') as fh: 
        lines = fh.readlines()

    if verbose: 
        print(f'Parsing {rpl_file}: ')
        for l in lines: 
            print(l)
    
    # get rid of spaces and newline characters 
    keys_and_values = dict([re.sub(' |\n', '', l).split('\t') for l in lines]) 
    
    width = int(keys_and_values['width'])
    height = int(keys_and_values['height'])
    depth = int(keys_and_values['depth']) 
    nbytes = int(keys_and_values['data-Length'])

    dtype = f'uint{nbytes*8}'
    shape = (height, width, depth)   

    return dtype, shape
    

class DataStack: 
        
    def __init__(self, datastack_file, mode='r', verbose=False, show_arrays=True): 
        '''Initialize DataStack object from *datastack_file*.''' 
        
        # default computation layers ordering as attributes  
        
        self.LAYERS = L.LAYERS 
        
        for l in L.LAYERS: 
            setattr(self, l, l.lower())
            
        # read datasets from file  
        
        self.mode = mode 
        self.datastack_file = datastack_file 
        
        self.update_attrs()
            
        # print tree 
        if verbose: 
            tree(self.datastack_file, show_arrays=show_arrays) 
            
    def update_attrs(self): 
        
        # populate store attributes 
        self.store = zarr.ZipStore(self.datastack_file, mode=self.mode) 
        self.root = zarr.group(store=self.store) 
        
        # generic exposure to dask arrays 
        self.datapath_list = sorted(self.root) 
        self.datasets = {dp: da.from_array(self.root[dp]) for dp in self.datapath_list}
        
        # attributify dask arrays 
        # useful for code development, perhaps confusing for users 
        # might turn off this feature later 
        for dp, ds in self.datasets.items(): 
            setattr(self, dp, ds) 
        
            
    def latest(self, datapath): 
        '''Return latest version of datapath. '''
        
        datapath = underscorify(datapath, self.datapath_list, extra_underscore=False)
        
        return datapath 
        
            
    def read(self, datapath, latest=True, compute=True):
        '''Read latest version of dataset for *datapath*
        
        Returns numpy array if dataset exists. Otherwise exits. '''
        
        if datapath in self.datapath_list: 
            if latest: 
                datapath = self.latest(datapath)     
            dataset = self.datasets[datapath] 
            if compute: 
                dataset = dataset.compute()
                
        # no dataset in file        
        else: 
            dataset = None 
            
            self.tree()
            assert False, f'Dataset not found: {datapath}'
    
        return dataset
    
    
    def read_list(self, datapath, latest=True, nan=-9999): 
        '''Thin wrapper for reading padded arrays (ragged lists). 

        Returns ragged list if dataset exists. Current implementation only for 
        two-dimensional (ragged) list of lists. ''' 

        # step 1: read (padded array 
        padded_array = self.read(datapath, latest=latest, compute=True)

        # step 2: convert to ragged list by removing nan values 
        ragged_list = _unstraighten(padded_array, nan=nan)

        return ragged_list 


    
    def tree(self, show_arrays=False): 
        '''Prints content tree of datastack.'''
        
        tree(self.datastack_file, show_arrays=show_arrays)
            

            
    def close(self): 
        '''Close file handle'''
         
        self.store.close()
        self.mode = 'closed' 
        
        print(f'Closed: {self.datastack_file}')             

def _straighten(ragged_list, nan=-9999): 
    '''Utility function to straighten a `ragged_list` of integers indices into a regular (padded) array. 
    
    
    Creates a two dimensional numpy array with empty values padded with nan=-9999. 
    
    Returns: padded_array 
    '''
    
    # determine shape 
    ncols = max([len(idxs) for idxs in ragged_list])
    nrows = len(ragged_list) 
    
    # initialize 
    padded_array = np.ones([nrows, ncols], dtype=int)
    padded_array[:,:] = nan 
    
    # fill 
    
    for i, indices in enumerate(ragged_list): 
        for j, idx in enumerate(indices): 
            padded_array[i, j] = idx 
        
    return padded_array 
    

def _unstraighten(padded_array, nan=-9999):
    '''Convert a numpy `padded_array` of integers filled out with nan's into a ragged list.
    
    
    Returns: a ragged list of lists 
    '''

    ragged_list = []
    
    for row in padded_array: 
        row_list = list(row[row!=nan]) # remove nan's from list  
        ragged_list.append(row_list)

    return ragged_list
    
   
