import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

import torch
from torch.utils.data import DataLoader, Subset, default_collate
# from torch.utils.tensorboard import SummaryWriter

from pyvtools.text import find_numbers, filter_by_string_must


def logL1f32(pred,target): # Smallest float32 is 1.175494 × 10-38
    return torch.mean(torch.log(torch.abs(pred-target)+1e-12))

def logL1f16(pred,target): # Smallest float16 is 6.10 × 10-5
    return torch.mean(torch.log(torch.abs(pred-target)+8e-5))

LOSS_FUNCTIONS = {
    "L1": torch.nn.L1Loss(),
    "L2": torch.nn.MSELoss(),
    "logL1f32": logL1f32,
    "logL1f16": logL1f16,

}

class DummyScaler:

    def scale(self, loss):
        return loss
    
    def step(self, optimizer):
        optimizer.step()
    
    def update(self):
        return

class Trainer:

    def __init__(self, model, loss_function, optimizer, data_manager, 
                 mixed_precision=False, path="models", debug=0):
        
        self.debug = debug
        
        self._model = model
        self._new_training_records()
        self._extract_model_properties()

        self.loss_function = loss_function
        self.optimizer = optimizer
        self.data_manager = data_manager

        self._setup_tensorflow()

        self.mixed_precision = mixed_precision
        # print("(!!!) Mixed precision is not currently implemented")
        # print("(!!!) Mixed precision is currently forced to torch.float16 on forward pass")

        self._path = path
        if not os.path.isdir(self.path): os.mkdir(self.path)
        self._folder = self.path

    def info(self, *args):
        if self.debug>=1: print(*args)

    def log(self, *args):
        if self.debug>=2: print(*args)

    def detail(self, *args):
        if self.debug>=3: print(*args)

    def _new_training_records(self):
        self._n_epochs_trained = 0
        self._n_batches_trained = 0
        self._last_train_loss = np.inf
        self._last_val_loss = np.inf
        self._best_train_loss = np.inf
        self._best_val_loss = np.inf
        self._change_train = 0
        self._change_val = 0
        self._curve_train_loss = []
        self._curve_val_loss = []
        self._curve_epochs = []

    @property
    def path(self):
        return self._path
    
    @path.setter
    def path(self, value):
        self._path = value
        if not os.path.isdir(): os.mkdir(value)
    
    def _get_timestamp(self):
        return datetime.now().strftime('%Y%m%d_%H%M%S')

    def _setup_tensorflow(self):
        # self._writer = SummaryWriter('runs/fashion_trainer_{}'.format(self._get_timestamp))
        return

    @property
    def writer(self):
        return self._writer

    @property
    def model(self):
        return self._model

    def _extract_model_properties(self):

        params = dict({k: p for k, p in self.model.named_parameters() if p.requires_grad})
        self._n_params = np.sum([p.numel() for p in params.values()])

        all_layers = []
        for k in params.keys():
            layer = k.split("weight")[0].split("bias")[0]
            if layer[-1]==".": layer = layer[:-1]
            all_layers.append(layer)
        
        layers = []
        for l in all_layers: 
            if l in all_layers and l not in layers: layers.append(l)
        self._layers = layers

        included = []
        new_params = {}
        for l in layers[::-1]: # reverse order is needed coz some layer names are included in others
            these_params = {}
            for k, p in params.items():
                if l in k and k not in included: 
                    these_params.update({k: p})
                    included.append(k)
            new_params.update({l: these_params})
        self._params = {l: {k:p for k, p in zip(list(pars.keys())[::-1], list(pars.values())[::-1])} 
                        for l, pars in zip(list(new_params.keys())[::-1], list(new_params.values())[::-1])}
        # Just in case, order is reverted back to the original order, matching the layer list

    @property
    def params(self):
        return self._params

    @property
    def n_params(self):
        return self._n_params
    
    @property
    def layers(self):
        return self._layers
    
    @property
    def n_layers(self):
        return len(self.layers)
    
    @property
    def gradients(self):
        return {l:{k:p.grad for k, p in lparams.items()} for l, lparams in self.params.items()}
        # (n_layers, 2, p_len) where 2 is for weights and biases, 
        # and p_len is either the length of the flatten weights or the number of biases

    @property
    def n_gradients(self):
        return int(np.sum([np.sum([g.numel() for g in grads.values()]) 
                           for grads in self.gradients.values()]))

    @property
    def n_epochs_trained(self):
        return self._n_epochs_trained
    
    @property
    def n_batches_trained(self):
        return self._n_batches_trained
    
    def _setup_start_training(self, n_samples_optimizer=1):
        self._n_samples_optimizer = n_samples_optimizer
        self._do_update_weights = False
        self.optimizer.zero_grad()
        if self.mixed_precision: 
            self.scaler = torch.GradScaler("cuda")
        else: self.scaler = DummyScaler()
    
    @property
    def n_samples_optimizer(self):
        return self._n_samples_optimizer
    
    @property
    def do_update_weights(self):
        return self._do_update_weights
    
    def _update_weights(self):

        if self.n_samples_optimizer==1:
            self._do_update_weights = True
        else:
            index = self.n_batches_trained + 1
            condition_1 = index/self.n_samples_optimizer == index//self.n_samples_optimizer
            condition_2 = index == self.data_manager.n_batch_train
            self._do_update_weights = condition_1 or condition_2

        if self.do_update_weights:
            
            # old_params = [[p.detach().cpu().numpy() for p in pars.values()] 
            #                 for pars in self.params.values()] # Numpy array, instead of tensors
            # self._check_gradient() # Examine the current gradient
            
            self.scaler.step(self.optimizer) # Adjust learning weights
            self.scaler.update() # Updates the scale for next iteration
            self.optimizer.zero_grad() # Zero the gradients after updating

            # new_params = [[p.detach().cpu().numpy() for p in pars.values()] 
            #                 for pars in self.params.values()] # Numpy array, instead of tensors
            # self._check_params(old_params, new_params) # Examine changes in parameters

    def _train_one_epoch(self):
        
        running_loss = 0.
        last_loss = 0.

        # Here, we use enumerate(training_loader) instead of
        # iter(training_loader) so that we can track the batch
        # index and do some intra-epoch reporting
        for batch_number, data in enumerate(self.data_manager.train_loader):

            # Every data instance is an input + label pair
            inputs, targets = data

            with torch.cuda.amp.autocast(enabled=self.mixed_precision):
            # with torch.autocast(device_type='cuda', dtype=torch.float16): # FORCEFULLY ACTIVATED
            # with torch.autocast(device_type='cuda'): # FORCEFULLY DEACTIVATED

                # Make predictions for this batch
                outputs = self.model(inputs)
                self.detail("Output range", torch.min(outputs), torch.max(outputs))

                # Compute the loss
                loss = self.loss_function(outputs, targets)

            # Compute the loss gradients
            self.scaler.scale(loss).backward()

            # Adjust learning weights
            self._update_weights()

            # Gather data and report
            last_loss = loss.item()
            running_loss += last_loss
            self._n_batches_trained += 1

            if self.do_update_weights: optimizer_log = ">>> Updated weights"
            else: optimizer_log = ""
            self.log(f"> Batch {batch_number+1}/{self.data_manager.n_batch_train} ", 
                     f">>> Avg Batch Loss: {last_loss}", optimizer_log)

        return running_loss / self.data_manager.n_batch_train
    
    def train(self, n_epochs, autostop=False, n_epochs_stop=8,
              threshold_changes=.001, threshold_overfitting=.85,
              n_samples_optimizer=1):

        self._set_directory()
        self.info("Starting training stored at... ", self._folder)
        self._setup_start_training(n_samples_optimizer)
        self._setup_stop_training(autostop, n_epochs_stop,
                                  threshold_changes, threshold_overfitting)
        self.data_manager.training = True

        for epoch_number in range(n_epochs):
            self.info(f'= EPOCH {epoch_number+1} ===============================')

            # Make sure gradient tracking is on
            self.model.train(True)

            # Keep records of previous loss values
            # previous_train_loss = float(self.last_train_loss)
            # previous_val_loss = float(self.last_val_loss)

            # Train one epoch
            self._n_batches_trained = 0
            self._last_train_loss = self._train_one_epoch()
            self._n_epochs_trained += 1

            # Set the model to evaluation mode, disabling dropout and using population
            # statistics for batch normalization.
            self.model.eval()

            # Disable gradient computation and reduce memory consumption.
            running_val_loss = 0.0
            with torch.no_grad():
                for vdata in self.data_manager.val_loader:
                    inputs_val, targets_val = vdata
                    outputs_val = self.model(inputs_val)
                    val_loss = self.loss_function(outputs_val, targets_val)
                    running_val_loss += val_loss
            self._last_val_loss = float(running_val_loss / self.data_manager.n_batch_val)

            # Log the running loss averaged per batch for both training and validation     
            self._curve_train_loss.append(self.last_train_loss)
            self._curve_val_loss.append(self.last_val_loss)
            self._curve_epochs.append(self.n_epochs_trained)
            # self.writer.add_scalars(
            #     'Training vs. Validation Loss',
            #     { 'Training' : self.last_train_loss, 
            #       'Validation' : self.last_val_loss },
            #     epoch_number + 1)
            # self.writer.flush()

            # Track best performance, and save the model's state
            self._change_val = self.last_val_loss - self.best_val_loss
            self._change_train = self.last_train_loss - self.best_train_loss
            do_save = False
            if self.change_train < 0:
                self._best_train_loss = self.last_train_loss
                do_save = True
            if self.change_val < 0:
                self._best_val_loss = self.last_val_loss
                do_save = True
            self.detail("Save?", do_save)
            if do_save:
                self.save()
                if self.check_to_stop_training():
                    break

            # Log the running loss averaged per batch for both training and validation
            # self.detail(">>> Avg Epoch Train Loss before?", previous_train_loss)
            # self.detail(">>> Avg Epoch Val Loss before?", previous_val_loss)
            self.info("=== Epoch End =========================================\n",
                    f">>> Avg Epoch Train Loss {self.last_train_loss}\n",
                    f">>> Avg Epoch Val Loss {self.last_val_loss}")
        
        self.save_trajectory()

        return

    @property
    def last_train_loss(self):
        return self._last_train_loss

    @property
    def last_val_loss(self):
        return self._last_val_loss

    @property
    def best_train_loss(self):
        return self._best_train_loss

    @property
    def best_val_loss(self):
        return self._best_val_loss
    
    @property
    def change_train(self):
        return self._change_train

    @property
    def change_val(self):
        return self._change_val
    
    @property
    def curve_train_loss(self):
        return self._curve_train_loss
    
    @property
    def curve_val_loss(self):
        return self._curve_val_loss

    @property
    def curve_epochs(self):
        return self._curve_epochs
    
    def _setup_stop_training(self, autostop, n_epochs_stop, 
                             threshold_changes, threshold_overfitting):

        self._autostop = autostop
        self._n_epochs_stop = n_epochs_stop
        self._n_epochs_stop_counter_val = 0
        self._n_epochs_stop_counter_train = 0
        self._threshold_changes = threshold_changes
        self._threshold_overfitting = threshold_overfitting - 1
    
    @property
    def autostop(self):
        return self._autostop

    @property
    def n_epochs_stop(self):
        return self._n_epochs_stop
    
    @property
    def n_epochs_stop_counter_train(self):
        return self._n_epochs_stop_counter_train
    
    @property
    def n_epochs_stop_counter_val(self):
        return self._n_epochs_stop_counter_val

    @property
    def threshold_changes(self):
        return self._threshold_changes
    
    @property
    def threshold_overfitting(self):
        return self._threshold_overfitting
    
    def check_to_stop_training(self):
        # Only triggered when a checkpoint is about to be saved

        if self.autostop:
            ratio = (self.last_train_loss - self.best_val_loss)/self.best_val_loss
            if ratio < self.threshold_overfitting:
                print("Training has stopped after detecting overfitting")
                return True
            else:
                if self.change_val < 0:
                    if -self.change_val/self.last_val_loss < self.threshold_changes:
                        self._n_epochs_stop_counter_val +=1
                    if self.n_epochs_stop_counter_val > self.n_epochs_stop:
                        print(f"Training has stopped because validation loss has ceased to improve")
                        return True
                    else:
                        return False
                else:
                    if -self.change_train/self.last_train_loss < self.threshold_changes:
                        self._n_epochs_stop_counter_train +=1
                    if self.n_epochs_stop_counter_train > self.n_epochs_stop:
                        print(f"Training has stopped because training loss has ceased to improve")
                        return True
                    else:
                        return False
        else:
            return False
    
    def plot_trajectory(self, save=True):

        plt.figure()
        plt.plot(self.curve_epochs, self.curve_train_loss, "D-", label="Training")
        plt.plot(self.curve_epochs, self.curve_val_loss, "o-C3", label="Validation")
        plt.xlabel("Epochs")
        plt.ylabel("Average Loss")
        plt.legend()
        plt.grid()

        if save:
            plt.savefig(self._get_filepath()[:-3]+"_Training.png", facecolor='w')
    
    def save_trajectory(self):

        array = np.array([self.curve_epochs, self.curve_train_loss, self.curve_val_loss])

        np.savetxt(self._get_filepath()[:-3]+"_Training.csv", array.T,
                   delimiter=",", header="Epochs, Training Loss, Validation Loss")

    def load_trajectory(self, folder_path=None):

        if folder_path is not None:
            self._folder = folder_path

        filenames = os.listdir(self._folder)
        filenames_trajectory = filter_by_string_must(filenames, ".csv")
        filenames = np.array(filter_by_string_must(filenames, ".pt"))

        values = np.array([find_numbers(fname) for fname in filenames])[:,-3:]
        # Columns should be: validation loss, training loss, epochs
        
        val_loss, train_loss, epochs = values.T
        indices = np.argsort(epochs)
        values = values[indices]
        filenames = filenames[indices]

        # Extract information from the last model
        last_filepath = os.path.join(self._folder, filenames[-1])
        last_checkpoint = torch.load(last_filepath)

        try:
            self._curve_epochs = last_checkpoint['curve_epochs']
            self._curve_train_loss = last_checkpoint['curve_train_loss']
            self._curve_val_loss = last_checkpoint['curve_val_loss']
        except:
            if len(filenames_trajectory)!=0:
                record_filepath = os.path.join(self._folder, filenames_trajectory[-1])
                array = np.loadtxt(record_filepath, delimiter=",", skiprows=1)
                epochs, train_loss, val_loss = array.T
                self._curve_epochs = list(epochs.astype(np.int32))
                self._curve_train_loss = list(train_loss)
                self._curve_val_loss = list(val_loss)
            else:
                self._curve_epochs = []
                self._curve_train_loss = []
                self._curve_val_loss = []
                self.log("No trajectory was found at folder path")
    
    def trim_trajectory(self, n_epochs_trained):
        if len(self.curve_epochs) != 0:
            indices = np.array(self.curve_epochs) > n_epochs_trained
            index = np.argmax(indices) 
            # First that needs to be discarded will be the first False
            if index != 0:
                self._curve_epochs = self.curve_epochs[:index]
                self._curve_train_loss = self.curve_train_loss[:index]
                self._curve_val_loss = self.curve_val_loss[:index]

    def _set_directory(self):
        folder = '{}_{}'.format(self.model._get_name(), 
                                self._get_timestamp())
        self._folder = os.path.join(self.path, folder)
        if not os.path.isdir(self._folder): os.mkdir(self._folder)

    def _get_filename(self):
        filename = '{}_V_{}_T_{}'.format(
            self.model._get_name(), 
            self.last_val_loss,
            self.last_train_loss
            )
        return filename

    def _get_filepath(self):
        filename = self._get_filename()
        filename += f'_{self.n_epochs_trained}.pt'
        return os.path.join(self._folder, filename)

    def save(self):

        torch.save({
            'model': self.model.state_dict(),
            'optimizer': self.optimizer.state_dict(),
            'last_train_loss': self.last_train_loss,
            'last_val_loss': self.last_val_loss,
            'best_train_loss': self.best_train_loss,
            'best_val_loss': self.best_val_loss,
            'n_epochs': self.n_epochs_trained,
            'curve_epochs': self.curve_epochs,
            'curve_train_loss': self.curve_train_loss,
            'curve_val_loss': self.curve_val_loss,
            'timestamp': self._get_timestamp(),
            }, self._get_filepath())

    def load(self, filepath):

        checkpoint = torch.load(filepath)
        self._folder = os.path.split(filepath)[0]
        
        self.model.load_state_dict(checkpoint['model'])
        self.optimizer.load_state_dict(checkpoint['optimizer'])

        self.detail(">>>>> Before Loading", self.last_train_loss)
        self._last_train_loss = checkpoint['last_train_loss']
        self._last_val_loss = checkpoint['last_val_loss']
        self._best_train_loss = checkpoint['best_train_loss']
        self._best_val_loss = checkpoint['best_val_loss']
        self.detail(">>>>> After Loading", self.last_train_loss)

        try:
            self._n_epochs_trained = checkpoint['n_epochs']
        except:
            self._n_epochs_trained = find_numbers(filepath)[-1]
        
        self.load_trajectory()
        self.trim_trajectory(self._n_epochs_trained)

        return
        
    def load_from_available(self, folder_path=None, 
                            discard_overfit=False, min_val_loss=False):
        """
        By default, returns last available checkpoint.

        If `min_val_loss`, then it looks for the checkpoint with minimum 
        validation loss.

        If `discard_overfit` is set to , then it discards all checkpoints 
        with training loss smaller than validation loss before selecting a 
        file using the chosen criteria.
        """

        if folder_path is not None:
            self._folder = folder_path

        self.load_trajectory()
        curve_epochs = np.array(self._curve_epochs)
        curve_train_loss = np.array(self._curve_train_loss)
        curve_val_loss = np.array(self._curve_val_loss)

        # To discard overfit, look for the whole trajectory first
        if discard_overfit:
            indices = curve_train_loss < curve_val_loss
            index = np.argmax(indices) # First with overfitting will be the first False
            if index != 0:
                n_epochs_overfit = curve_epochs[index]
                self.info(f"# Overfit starts on epoch {n_epochs_overfit:.0f}")
            else:
                n_epochs_overfit = None
                self.info("# No overfitting detected in the trajectory")

        # Then, go and look what is available in the folder
        filenames = os.listdir(self._folder)
        filenames = np.array(filter_by_string_must(filenames, ".pt"))

        values = np.array([find_numbers(fname) for fname in filenames])[:,-3:]
        # Columns should be: validation loss, training loss, epochs
        
        val_loss, train_loss, epochs = values.T
        indices = np.argsort(epochs)
        values = values[indices]
        filenames = filenames[indices]

        val_loss, train_loss, epochs = values.T
        if discard_overfit and n_epochs_overfit is not None:
            indices = epochs >= n_epochs_overfit
            index_overfit = np.argmax(indices) # First with overfitting will be the first False
            if index_overfit != 0:
                self.info(f"# First available with overfit is {epochs[index_overfit]:.0f}")
                values = values[:index_overfit]
                filenames = filenames[:index_overfit]
            else:
                self.info("# No checkpoint with overfit is available")

        val_loss, train_loss, epochs = values.T
        if min_val_loss:
            index = np.argmin(val_loss)
        else:
            index = -1
        
        filepath = os.path.join(self._folder, filenames[index])
        self.info("Loading", filepath)
        self.load( filepath )

    def predict(self, x):

        self.model.eval()
        self.data_manager.training = False
        with torch.no_grad():
            if x.dim() < 4:
                return self.model(x.unsqueeze(0)).squeeze()
            else:
                return self.model(x)
    
    def test(self):

        self.info('= TEST ===============================================')

        # Set the model to evaluation mode, disabling dropout and using population
        # statistics for batch normalization.
        self.model.eval()
        self.data_manager.training = False
        self.info("> Loss Function", self.loss_function._get_name())

        # Disable gradient computation and reduce memory consumption.
        running_loss = 0.0
        with torch.no_grad():
            for i, data in enumerate(self.data_manager.test_loader):
                inputs, targets = data
                outputs = self.model(inputs)
                loss = self.loss_function(outputs, targets)
                self.log(f"> Batch {i+1}/{self.data_manager.n_batch_test} ", 
                        f">>> Avg Batch Loss: {loss}")
                running_loss += loss
        avg_loss = running_loss / self.data_manager.n_batch_test

        self.info(f">>> Avg Test Loss {float(avg_loss)}")

        return float(avg_loss)
    
    def _check_gradient(self):
        
        gradient = [[g.detach().cpu().numpy() for g in grads.values()] 
                    for grads in self.gradients.values()] # Numpy array, instead of tensors
        
        n_non_zero = np.sum([np.sum([np.sum(g!=0) for g in grads]) for grads in gradient])
        
        indices = [[np.argmax(np.abs(g.flatten())) for g in grads] for grads in gradient]
        max_grad_values = [[g.flatten()[ind] for g, ind in zip(grads, inds)]
                            for grads, inds in zip(gradient, indices)]
        
        layers = []
        for l, inds in zip(self.layers, indices):
            if inds != [0,0]:
                layers.append(l)

        self.detail(f">>> Gradient has {self.n_gradients} elements for {self.n_params} parameters")
        self.detail(">>> Number of non-zero elements in the gradient?", 
                    f"{n_non_zero*100/self.n_gradients:.6f}%")
        self.detail(">>> Max values are...", max_grad_values)
        self.detail(">>> Layers with non-zero gradient are...", layers)

    def _check_params(self, old_params, new_params):

        # Params must be dettached numpy array versions of self.params
        n_changed = np.sum([np.sum([np.sum(o!=n) for o, n in zip(old, new)]) 
                            for old, new in zip(old_params, new_params)])
        indices = [[np.argmax(np.abs(o-n).flatten()) for o, n in zip(old, new)] 
                    for old, new in zip(old_params, new_params)]
        change = [[n.flatten()[i] - o.flatten()[i] for o, n, i in zip(old, new, ind)] 
                    for old, new, ind in zip(old_params, new_params, indices)]
    
        layers = []
        for l, inds in zip(self.layers, indices):
            if inds != [0,0]:
                layers.append(l)

        self.detail(">>> Have the model parameters changed?", n_changed!=0)
        self.detail(">>> Which fraction of them changed?", 
                    f"{n_changed*100/self.n_params:.4f}%")
        self.detail(">>> Max change per layer is...", change)
        self.detail(">>> Layers with parameter changes are...", layers)