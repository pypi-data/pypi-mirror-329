import torch

#%% LOGGING

def print_debug(*args, debug:bool=False):
    if debug: print(*args)

class Logger:

    def __init__(self, debug:bool=False):
        self.debug=debug
    
    def log(self, *args):
        if self.debug: print(*args)

class LevelsLogger:

    def __init__(self, debug:int=0):
        self.debug = debug

    def info(self, *args):
        if self.debug>=1: print(*args)

    def log(self, *args):
        if self.debug>=2: print(*args)

    def detail(self, *args):
        if self.debug>=3: print(*args)

#%% CUDA/GPU SUPPORT

def get_device(pick_last=True, debug=False):
    if torch.cuda.is_available():
        # CUDA is available, use the last CUDA device (assume the first one is used by the system)
        devices = [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())]
        if len(devices) > 1: 
            if pick_last: 
                torch.cuda.set_device( len(devices)-1 )
                print_debug("GPUs", devices, "(last is selected)", debug=debug)
            else:
                print_debug("GPUs", devices, "(first is selected", debug=debug)
        else: print_debug("GPU", devices[0], debug=debug)
        return torch.device("cuda")
    elif torch.backends.mps.is_available():
        # CUDA is not available, but MPS is available (Apple Silicon GPUs), use MPS device
        print_debug("MPS", debug=debug)
        return torch.device("mps")
    else:
        # Neither CUDA nor MPS is available, use the CPU
        print_debug("CPU", debug=debug)
        return torch.device("cpu")
