import os

import numpy as np
from pathlib import Path
import h5py
import pickle as pick
from tqdm import tqdm

import torch
from torch.utils.data import Dataset as TorchDataset
from torch.utils.data import DataLoader, Subset, default_collate
# import torchvision.transforms as T
import torchvision.transforms.v2 as v2

from pyvtools.text import find_numbers
import pyvtorch.aux as vtaux
import pyvtools.image as vim
import pyvtorch.image as vtim

#%% DATASET UTILITIES

def identity(x): 
    return x

def check_dataset_consistency(filenames_x, filenames_y=None):
    """Check if the x filenames list matches with y filenames list"""

    is_paired = filenames_y is not None

    file_type_x = os.path.splitext(filenames_x[0])[1].lower()
    if is_paired: 
        file_type_y = os.path.splitext(filenames_y[0])[1].lower()
        assert len(filenames_x) == len(filenames_y), "Images / masks length mismatch"

    assert not np.all([file_type_x in filenames_x]), "There is an X file that has the wrong extension"
    if is_paired:
        assert not np.all([file_type_y in filenames_y]), "There is an Y file that has the wrong extension"
        filename_y_numbers = [find_numbers(fname) for fname in filenames_y]
        for fname in filenames_x:
            numbers_x = find_numbers(fname)
            assert numbers_x in filename_y_numbers, f"/X {fname}'s Y pair has not be found"

#%% DATASET CLASSES

class PairsDataset(TorchDataset):
    """
    Initialization
    --------------
    Given a pair of directories...
    (1) List all available files inside those directories
    (2) Check that all files are paired
    (3) Count the number N of datapoints
    (4) Run raw preprocessing set-up [Optional]
    (4) Run transform set-up [Optional]
    (5) Run model preprocessing set-up [Optional]

    Preprocessing set-up is run on raw data, without applying any 
    preprocessing nor transforms. The configured raw preprocessing 
    strategy is usually meant to deliver data for human vizualisation.

    Transform set-up is run only on preprocessed data, without 
    applying any transforms nor the training preprocessing. The 
    transformed data can include, for example, rotations or translations 
    that are not originally present in the data.

    Model preprocessing set-up is run on transformed preprocessed data. 
    The configured model preprocessing strategy is usually meant to 
    deliver data straight to the model, no longer necessarily fit for 
    human visualization.

    Loading data
    ------------
    Given an integer 0<=i<N representing a datapoint ID...
    (1) Filepath is determined (default: path to the ith available file)
    (2) Datapoint pair is loaded (default: load image as Numpy array)
    (3) Run raw preprocessing (default: do nothing)
    (4) Run transformations (default: do nothing)
    (5) Run training preprocessing (default: convert to Tensorflow tensor)
    """


    def __init__(self,
        x_dir: str=None,
        y_dir: str=None,
        transform=None,
        device=None,
    ):
        self.__data_loading_init__(x_dir, y_dir)
        self.__standard_init__(transform, device)
    
    def __data_loading_init__(self, x_dir, y_dir):

        self._x_dir = x_dir
        self._y_dir = y_dir

        self._x_list = self.__list_files_x__()
        self._y_list = self.__list_files_y__()

    @property
    def directory(self):
        return os.path.commonpath([self.x_dir, self.y_dir])

    @property
    def folder(self):
        return os.path.split(self.directory)[-1]
    
    @property
    def x_dir(self):
        return self._x_dir

    @property
    def y_dir(self):
        return self._y_dir

    def __repr__(self):
        rep = (
            f"{type(self).__name__}: {(self.folder)} dataset with {len(self)} pairs"
        )
        for n, (x, y) in enumerate(zip(self.x_list, self.y_list)):
            rep += f"\nX_{n}: {Path(x).name}\tY_{n}: {Path(y).name}"
            if n > 10:
                rep += "\n..."
                break
        return rep
        
    def __list_files_x__(self):
        return sorted(os.listdir(self.x_dir))

    def __list_files_y__(self):
        return sorted(os.listdir(self.y_dir))
    
    def __standard_init__(self, transform, device):

        if transform is None: self.transform = identity
        else: self.transform = transform

        if device is None: self.device = vtaux.get_device()
        else: self.device = device

        self._n_instances = self.__count_instances__()
        self.__check_consistency__()
        self._n_datapoints = self.__count_datapoints__()

        self._x_ids = self.__list_ids_x__()
        self._y_ids = self.__list_ids_y__()

        assert len(self.x_ids) == self.n_datapoints, "Not enough x IDs for x datapoints"
        assert len(self.y_ids) == self.n_datapoints, "Not enough y IDs for y datapoints"

        # Initialise as identity functions
        self._preprocess_raw_x = identity
        self._preprocess_raw_y = identity
        self._preprocess_raw_inverse_x = identity
        self._preprocess_raw_inverse_y = identity
        self._apply_augmentations = identity
        self._preprocess_for_model_x = identity
        self._preprocess_for_model_y = identity
        self._preprocess_for_model_inverse_x = identity
        self._preprocess_for_model_inverse_y = identity
        # Then configure them, stage by stage

        self.__set_up_raw_preprocessing__()
        self._preprocess_raw_x = lambda x : self.preprocess_raw_x(x)
        self._preprocess_raw_y = lambda y : self.preprocess_raw_y(y)
        self._preprocess_raw_inverse_x = lambda x : self.preprocess_raw_inverse_x(x)
        self._preprocess_raw_inverse_y = lambda y : self.preprocess_raw_inverse_y(y)

        self.__set_up_transforming__()
        self._apply_augmentations = lambda args : self.apply_augmentations(args)

        self.__set_up_model_preprocessing__()
        self._preprocess_for_model_x = lambda x : self.preprocess_for_model_x(x)
        self._preprocess_for_model_y = lambda y : self.preprocess_for_model_y(y)
        self._preprocess_for_model_inverse_x = lambda x : self.preprocess_for_model_inverse_x(x)
        self._preprocess_for_model_inverse_y = lambda y : self.preprocess_for_model_inverse_y(y)

        self._training = False
        self.training = False

    @property
    def x_list(self):
        return self._x_list

    @property
    def y_list(self):
        return self._y_list

    def __count_instances__(self):
        return len(self.x_list)

    @property
    def n_instances(self):
        return self._n_instances

    def __check_consistency__(self):
        check_dataset_consistency(self.x_list, self.y_list)

    def __count_datapoints__(self):
        return self.n_instances

    @property
    def n_datapoints(self):
        return self._n_datapoints

    def __len__(self):
        return self.n_datapoints

    @property
    def x_ids(self):
        return self._x_ids

    @property
    def y_ids(self):
        return self._y_ids

    def __list_ids_x__(self):
        return list(range(self.n_datapoints))

    def __list_ids_y__(self):
        return list(range(self.n_datapoints))

    def filename_x(self, id):
        return self.x_list[self.x_ids[id]] # return self.x_list[id]

    def filename_y(self, id):
        return self.y_list[self.y_ids[id]] # return self.y_list[id]

    def filepath_x(self, id):
        return os.path.join(self.x_dir, self.filename_x(id))
    
    def filepath_y(self, id):
        return os.path.join(self.y_dir, self.filename_y(id))

    def load_x(self, id):
        return vim.load_image(self.filepath_x(id)) # Loads as float32 Numpy array
    
    def load_y(self, id):
        return vim.load_image(self.filepath_y(id)) # Loads as float32 Numpy array
    
    def __set_up_raw_preprocessing__(self):
        return

    def preprocess_raw_x(self, x):
        return x
    
    def preprocess_raw_y(self, y):
        return y

    def preprocess_raw_inverse_x(self, x):
        return x
    
    def preprocess_raw_inverse_y(self, y):
        return y

    def __set_up_transforming__(self):
        return

    def apply_augmentations(self, data): # x, y = data
        return self.transform(data)

    @property
    def training(self):
        return self._training
    
    @training.setter
    def training(self, value):

        # Only apply augmentations while training
        if value: 
            self._apply_augmentations = lambda args : self.apply_augmentations(args)
        else: 
            self._apply_augmentations = identity
        
        self._training = value

    def __set_up_model_preprocessing__(self):
        return

    def preprocess_for_model_x(self, x):
        return torch.from_numpy(x.transpose(2, 0, 1)).to(self.device) # Results on a (C, H, W) Torch tensor
    
    def preprocess_for_model_y(self, y):
        return torch.from_numpy(y.transpose(2, 0, 1)).to(self.device) # Results on a (C, H, W) Torch tensor
    
    def preprocess_for_model_inverse_x(self, x):
        return x.cpu().detach().numpy().transpose(1,2,0) # Results on a (H, W, C) Numpy array
    
    def preprocess_for_model_inverse_y(self, y):
        return y.cpu().detach().numpy().transpose(1,2,0) # Results on a (H, W, C) Numpy array
    
    def __getitem__(self, idx):

        x = self.load_x(idx)
        y = self.load_y(idx)

        x = self._preprocess_raw_x(x)
        y = self._preprocess_raw_y(y)

        x, y = self._apply_augmentations((x, y))
        
        x = self._preprocess_for_model_x(x)
        y = self._preprocess_for_model_y(y)

        return x, y

    def load(self, idx):
        
        return self[idx]

    def preview(self, idx):

        x = self.load_x(idx)
        y = self.load_y(idx)

        x = self._preprocess_raw_x(x)
        y = self._preprocess_raw_y(y)

        return x, y

class PairsHDFDataset(PairsDataset):
    """
    Initialization
    --------------
    Given the filepath to an HDF file and the keys to its x and y data...
    (1) Count the total number M of x instances
    (2) Check that all there are the same number of x and y instances
    (3) Count the number N of datapoints
    (4) Run raw preprocessing set-up [Optional]
    (4) Run transform set-up [Optional]
    (5) Run model preprocessing set-up [Optional]

    Preprocessing set-up is run on raw data, without applying any 
    preprocessing nor transforms. The configured raw preprocessing 
    strategy is usually meant to deliver data for human vizualisation.

    Transform set-up is run only on preprocessed data, without 
    applying any transforms nor the training preprocessing. The 
    transformed data can include, for example, rotations or translations 
    that are not originally present in the data.

    Model preprocessing set-up is run on transformed preprocessed data. 
    The configured model preprocessing strategy is usually meant to 
    deliver data straight to the model, no longer necessarily fit for 
    human visualization.

    Loading data
    ------------
    Given an integer 0<=i<N representing a datapoint ID...
    (1) Filepath is determined (default: path to the ith available file)
    (2) Datapoint pair is loaded (default: load image as Numpy array)
    (3) Run raw preprocessing (default: do nothing)
    (4) Run transformations (default: do nothing)
    (5) Run training preprocessing (default: convert to Tensorflow tensor)
    """


    def __init__(self,
        filepath: str,
        x_key: str,
        y_key: str,
        transform=None,
        device=None,
    ):
        self.__data_loading_init__(filepath, x_key, y_key)
        self.__standard_init__(transform, device)

    def __data_loading_init__(self, filepath, x_key, y_key):
        self._filepath = filepath
        self._x_key = x_key
        self._y_key = y_key
        self._is_open = False
        self.open()

    @property
    def filepath(self):
        return self._filepath
    
    @property
    def directory(self):
        return os.path.join(os.path.split(self.filepath)[:-1])

    @property
    def x_key(self):
        return self._x_key

    @property
    def y_key(self):
        return self._y_key

    def __repr__(self):
        rep = (
            f"{type(self).__name__}: {(self.folder)} dataset with {len(self)} pairs"
        )
        for n, (x, y) in enumerate(zip(self.x_list, self.y_list)):
            rep += f"\nX_{n}: {Path(x).name}\tY_{n}: {Path(y).name}"
            if n > 10:
                rep += "\n..."
                break
        return rep
    
    def open(self):
        if not self._is_open:
            self._file =  h5py.File(self.filepath, "r")
        self._is_open = True
    
    def is_open(self):
        return self._is_open

    def __enter__(self):
        self.open()
        return self.file

    @property
    def file(self):
        return self._file
    
    def close(self):
        if self._is_open: self.file.close()
        self._is_open = False
    
    def __exit__(self, type, value, traceback):
        self.close()

    def __count_instances__(self):
        n_instances = self.file[self.x_key].shape[0]
        return n_instances

    @property
    def n_instances(self):
        return self._n_instances

    def __check_consistency__(self):
        assert self.file[self.x_key].shape[0] == self.file[self.y_key].shape[0]

    def __count_datapoints__(self):
        return self.n_instances
    
    def load_x(self, id):
        return np.array(self.file[self.x_key][id], dtype=np.float32) # Loads as float32 Numpy array
    
    def load_y(self, id):
        return np.array(self.file[self.y_key][id], dtype=np.float32) # Loads as float32 Numpy array

#%% DATASET MANAGER

class DataManager:

    def __init__(self, dataset, # val_dataset=None, test_dataset=None,
                 train_fraction=0.9, val_fraction=0.1, 
                 batch_size=128, batch_transform=None, debug=0):
        
        self.debug = debug

        self._dataset = dataset

        self._train_fraction = train_fraction
        self._val_fraction = val_fraction
        self._batch_size = batch_size

        if batch_transform is None:
            self.batch_transform = identity
        else:
            self.batch_transform = batch_transform

        self._apply_batch_augmentations = identity
        self._create_subdatasets() #TODO: Remember to update style to __blah__
        self.__update_dataset__()
        self._apply_batch_augmentations = lambda batch : self.apply_batch_augmentations(batch)

        self._training = False
        self.training = False

    def info(self, *args):
        if self.debug>=1: print(*args)

    def log(self, *args):
        if self.debug>=2: print(*args)

    def detail(self, *args):
        if self.debug>=3: print(*args)

    @property
    def dataset(self):
        return self._dataset

    @dataset.setter
    def dataset(self, value):
        self._dataset = value
        self._create_subdatasets()

    @property
    def n_total(self):
        return len(self.dataset)

    @property
    def train_fraction(self):
        return self._train_fraction

    @train_fraction.setter
    def train_fraction(self, value):
        self._train_fraction = value
        self._create_subdatasets()
    
    @property
    def val_fraction(self):
        return self._val_fraction

    @val_fraction.setter
    def val_fraction(self, value):
        self._val_fraction = value
        self._create_subdatasets()

    @property
    def batch_size(self):
        return self._batch_size
    
    @batch_size.setter
    def batch_size(self, value):
        self._batch_size = value
        self._create_dataloaders()

    def _create_subdatasets(self):

        n_test = int(np.round((1-self.train_fraction) * self.n_total))
        n_val = int(np.round(self.val_fraction * (self.n_total - n_test)))
        n_train = self.n_total - n_test - n_val

        train_indices = np.arange(n_train)
        val_indices = np.arange(n_train, n_train+n_val)
        test_indices = np.arange(self.n_total-n_test, self.n_total)

        self._train_dataset = Subset(self.dataset, train_indices)
        self._val_dataset = Subset(self.dataset, val_indices)
        self._test_dataset = Subset(self.dataset, test_indices)

        self._create_dataloaders()

    def _create_dataloaders(self):
        self._train_loader = DataLoader(self.train_dataset, 
                                        batch_size=self.batch_size,
                                        collate_fn=self._collate_batch,
                                        shuffle=True)
        self._val_loader = DataLoader(self.val_dataset, 
                                      batch_size=self.batch_size,
                                      collate_fn=self._collate_batch,
                                      shuffle=True)
        self._test_loader = DataLoader(self.test_dataset, 
                                       batch_size=self.batch_size,
                                       shuffle=True)

    @property
    def train_dataset(self):
        return self._train_dataset

    @property
    def val_dataset(self):
        return self._val_dataset

    @property
    def test_dataset(self):
        return self._test_dataset

    @property
    def n_train(self):
        return len(self.train_dataset)

    @property
    def n_val(self):
        return len(self.val_dataset)

    @property
    def n_test(self):
        return len(self.test_dataset)

    @property
    def train_loader(self):
        return self._train_loader

    @property
    def val_loader(self):
        return self._val_loader

    @property
    def test_loader(self):
        return self._test_loader
    
    @property
    def n_batch_train(self):
        return len(self.train_loader)
    
    @property
    def n_batch_val(self):
        return len(self.val_loader)
    
    @property
    def n_batch_test(self):
        return len(self.test_loader)

    def __update_dataset__(self):
        return
    
    def apply_batch_augmentations(self, batch):
        return self.batch_transform(batch)

    def _collate_batch(self, batch):
        batch = default_collate(batch)
        batch = self._apply_batch_augmentations(batch)
        return batch

    @property
    def training(self):
        return self._training

    @training.setter
    def training(self, value):

        # Only apply augmentations while training
        self.dataset.training = value
        # self.train_dataset.training = value
        # self.test_dataset.training = value
        # self.val_dataset.training = value

        # Only apply batch transform while training
        if value: 
            self._apply_batch_augmentations = lambda batch : self.apply_batch_augmentations(batch)
        else:
            self._apply_batch_augmentations = identity

        # Remember state
        self._training = value

class NormalizingDataManager(DataManager):

    def __init__(self, dataset, # val_dataset=None, test_dataset=None,
                 train_fraction=0.9, val_fraction=0.1, 
                 batch_size=128, batch_transform=None, debug=0, 
                 regression=False):
        
        self._regression = regression

        super().__init__(
            dataset=dataset, # val_dataset=val_dataset, test_dataset=test_dataset,
            train_fraction=train_fraction, val_fraction=val_fraction, 
            batch_size=batch_size, batch_transform=batch_transform, debug=debug
        )

    @property
    def regression(self):
        return self._regression

    @property
    def stats_filepath(self):
        return os.path.splitext(self.dataset.filepath)[-2] + "stats.pkl"
    
    def __set_up_normalization__(self):
        
        self._load_stats()
        if not self.has_stats: 
            stats = self._calculate_stats()
            self._save_stats(stats)
            self._set_stats(stats)

        self.normalise_x = lambda x : (x-self.x_mean)/self.x_std
        self.normalise_inverse_x = lambda x : x*self.x_std+self.x_mean

        if self.regression:
            self.normalise_y = lambda y : (y-self.x_mean)/self.y_std
            self.normalise_inverse_y = lambda y : y*self.y_std+self.y_mean

    def __update_dataset__(self):

        self.__set_up_normalization__()
        
        self.dataset._preprocess_raw_x = lambda x : self.normalise_x(
            self.dataset.preprocess_raw_x(x) )
        self.dataset._preprocess_raw_inverse_x = lambda x : self.dataset.preprocess_raw_inverse_x(
            self.normalise_inverse_x(x) )

        if self.regression:
            self.dataset._preprocess_raw_y = lambda y : self.normalise_y(
                self.dataset.preprocess_raw_y(y) )
            self.dataset._preprocess_raw_inverse_y = lambda y : self.dataset.preprocess_raw_inverse_y(
                self.normalise_inverse_y(y) )
    
    def _set_stats(self, stats):

        self.x_shape = stats["x_shape"]
        self.x_dim = stats["x_dim"]

        self.all_x_min = stats["all_x_min"]
        self.all_x_max = stats["all_x_max"]
        self.all_x_mean = stats["all_x_mean"]
        self.all_stds_x = stats["all_stds_x"]

        self.x_min = stats["x_min"]
        self.x_max = stats["x_max"]
        self.x_mean = stats["x_mean"]
        self.x_std = stats["x_std"]

        print("> Newly set stats")
        print("X Min & Max", (self.x_min, self.x_max))
        print("X Mean", self.x_mean)
        print("X Std", self.x_std)

        if self.regression:

            self.y_shape = stats["y_shape"]
            self.y_dim = stats["y_dim"]

            self.all_y_min = stats["all_y_min"]
            self.all_y_max = stats["all_y_max"]
            self.all_y_mean = stats["all_y_mean"]
            self.all_stds_y = stats["all_stds_y"]
            
            self.y_min = stats["y_min"]
            self.y_max = stats["y_max"]
            self.y_mean = stats["y_mean"]
            self.y_std = stats["y_std"]

            print("Y Min & Max", (self.y_min, self.y_max))
            print("Y Mean", self.y_mean)
            print("Y Std", self.y_std)

        self.has_stats = True

    def _load_stats(self):
        
        try:
            with open(self.stats_filepath, 'rb') as f:
                stats = pick.load(f)
        except:
            stats = {}

        if stats != {}:
            self._set_stats(stats)
            self.has_stats = True
        else: self.has_stats = False
    
    def _save_stats(self, stats):
        with open(self.stats_filepath, 'wb') as f:
            pick.dump(stats, f)

    def _calculate_stats(self):

        stats = {}

        all_x_min, all_x_max = [], []
        all_x_mean, all_x_sqs_mean = [], []
        if self.regression:
            all_y_min, all_y_max = [], []
            all_y_mean, all_y_sqs_mean = [], []

        for index in tqdm(range(self.n_train)):
            x, y = self.train_dataset.__getitem__(index)
            all_x_min.append(float(x.min()))
            all_x_max.append(float(x.max()))
            all_x_mean.append(np.array(*[torch.mean(x, axis=(1,2)).detach().cpu()]))
            all_x_sqs_mean.append(np.array(*[torch.mean(x**2, axis=(1,2)).detach().cpu()]))
            if self.regression:
                all_y_min.append(float(y.min()))
                all_y_max.append(float(y.max()))
                all_y_mean.append(np.array(*[torch.mean(y, axis=(1,2)).detach().cpu()]))
                all_y_sqs_mean.append(np.array(*[torch.mean(y**2, axis=(1,2)).detach().cpu()]))
        
        x_shape = self._determine_shape_x(x)
        stats["x_shape"] = x_shape
        stats["x_dim"] = x.ndim
        if self.regression:
            y_shape = self._determine_shape_y(y)
            stats["y_shape"] = y_shape
            stats["y_dim"] = y.ndim
        del x, y
        
        stats["all_x_min"] = np.array(all_x_min)
        stats["all_x_max"] = np.array(all_x_max)
        stats["all_x_mean"] = np.array(all_x_mean)
        stats["all_stds_x"] = np.sqrt( np.array(all_x_sqs_mean) - stats["all_x_mean"]**2 )

        stats["x_min"] = np.min(all_x_min); stats["x_max"] = np.max(all_x_max)
        stats["x_mean"] = np.mean(all_x_mean, axis=0)
        stats["x_std"] = np.sqrt( np.mean(all_x_sqs_mean, axis=0) - stats["x_mean"]**2 )

        if self.regression:

            stats["all_y_min"] = np.array(all_y_min)
            stats["all_y_max"] = np.array(all_y_max)
            stats["all_y_mean"] = np.array(all_y_mean)
            stats["all_stds_y"] = np.sqrt( np.array(all_y_sqs_mean) - stats["all_y_mean"]**2 )

            stats["y_min"] = np.min(all_y_min); stats["y_max"] = np.max(all_y_max)
            stats["y_mean"] = np.mean(all_y_mean, axis=0)
            stats["y_std"] = np.sqrt( np.mean(all_y_sqs_mean, axis=0) - stats["y_mean"]**2 )
            
        return stats

    def _determine_shape_x(self, preprocessed_x):
        # Postprocessing converts (H,W,C) Numpy arrays into (C,H,W) Torch tensors
        x_shape = preprocessed_x.shape
        x_shape = (x_shape[-1], *x_shape[:2])
        return x_shape

    def _determine_shape_y(self, preprocessed_y):
        # Postprocessing converts (H,W,C) Numpy arrays into (C,H,W) Torch tensors
        y_shape = preprocessed_y.shape
        y_shape = (y_shape[-1], *y_shape[:2])
        return y_shape

    def _get_stats(self):

        stats = {}

        stats["x_shape"] = self.x_shape
        stats["x_dim"] = self.x_dim

        stats["all_x_min"] = self.all_x_min
        stats["all_x_max"] = self.all_x_max
        stats["all_x_mean"] = self.all_x_mean
        stats["all_stds_x"] = self.all_stds_x

        stats["x_min"] = self.x_min
        stats["x_max"] = self.x_max
        stats["x_mean"] = self.x_mean
        stats["x_std"] = self.x_std

        if self.regression:

            stats["y_shape"] = self.y_shape
            stats["y_dim"] = self.y_dim

            stats["all_y_min"] = self.all_y_min
            stats["all_y_max"] = self.all_y_max
            stats["all_y_mean"] = self.all_y_mean
            stats["all_stds_y"] = self.all_stds_y

            stats["y_min"] = self.y_min
            stats["y_max"] = self.y_max
            stats["y_mean"] = self.y_mean
            stats["y_std"] = self.y_std
        
        return stats
    
    @property
    def stats(self):
        return self._get_stats()