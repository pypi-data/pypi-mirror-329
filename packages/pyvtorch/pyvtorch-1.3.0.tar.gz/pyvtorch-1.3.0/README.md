# PyVTorch

General custom tools to work in deep learning research using Python and PyTorch

## Getting Started

### Installation

This package can easily be installed using `pip`:

```bash
pip install pyvtorch
```

An alternative installation that partially uses Anaconda would involve...

1. First, install some Anaconda distribution, in case you do not have any:
   https://docs.anaconda.com/anaconda/install/
2. Then, create an Anaconda environment with Python
   ```bash
   conda create -n dev python
   ```
3. Activate the environment
   ```bash
   conda activate dev
   ```
3. Then, install all required packages by running the `install.sh` script:
   ```bash
   yes | . install.sh
   ```
4. You can make sure that your PyTorch installation has CUDA GPU support by running...
   ```bash
   python -c "import torch; print(torch.cuda.is_available()) \
              print([torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())])"  
   ```
   The first line should print `True` if CUDA is supported. And the second line should show you the name/s of your available GPU/s.
5. That's it! You're good to go :)

That second installation procedure is designed to be overly redundant, so please feel free to follow your own installation procedure.

### Requirements

Provided installation steps are only guaranteed to work in Ubuntu 24.04 with NVidia drivers 535.

## Additional information

### Main Author Contact

Valeria Pais - @vrpais - valeriarpais@gmail.com