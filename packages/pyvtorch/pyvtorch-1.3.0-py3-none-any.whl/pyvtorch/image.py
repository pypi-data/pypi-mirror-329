import torch
import torchvision.transforms as T
import numpy as np
from math import log10, sqrt
from skimage.metrics import structural_similarity
from typing import Union

import pyvtools.image as vim
import pyvtorch.aux as vtaux


#%% IMAGE FORMAT

def numpy2torch(image:np.ndarray, device=vtaux.get_device(), dtype=torch.float32):

    return T.ToTensor()(image).to(device).type(dtype)

#%% IMAGE LOADING AND STORING

def load_rgb_image(filepath:str, device=vtaux.get_device(), dtype=torch.float32):
    """Loads an RGB image as a PyTorch Tensor

    Parameters
    ----------
    filepath : str
        Filepath to image
    device : torch.device, optional
        Device on which the output tensor will be allocated.
    dtype : torch.dtype, optional
        Desired output data type. Default is `torch.float32`.
    
    Returns
    -------
    RGB image as a PyTorch tensor (not BGR)

    See also
    --------
    vim.load_rgb_image
    vtaux.get_device
    """
    
    return numpy2torch(vim.load_rgb_image(filepath), device, dtype)

def load_tiff_image(filepath:str, device=vtaux.get_device(), dtype=torch.float32):
    """Loads a TIFF image as a PyTorch Tensor

    Parameters
    ----------
    filepath : str
        Filepath to image
    device : torch.device, optional
        Device on which the output tensor will be allocated.
    dtype : torch.dtype, optional
        Desired output data type. Default is `torch.float32`.
    
    Returns
    -------
    Image as a PyTorch tensor (probably RGGB)

    See also
    --------
    vim.load_tiff_image
    vtaux.get_device
    """
    
    return numpy2torch(vim.load_tiff_image(filepath), device, dtype)

def load_npy_image(filepath : str, device=vtaux.get_device(), dtype=torch.float32):
    """Loads an image saved as .npy into a PyTorch Tensor

    Parameters
    ----------
    filepath : str
        Filepath to image, must have ".npy" extension
    device : torch.device, optional
        Device on which the output tensor will be allocated.
    dtype : torch.dtype, optional
        Desired output data type. Default is `torch.float32`.
    
    Returns
    -------
    Image as a PyTorch tensor (probably RGGB)

    See also
    --------
    vim.load_npy_image
    vtaux.get_device
    """
    
    return numpy2torch(vim.load_npy_image(filepath), device, dtype)

def load_image(filepath:str, device=vtaux.get_device(), dtype=torch.float32):
    """Loads an image as a PyTorch tensor

    Currently supported formats: jpg, png, tiff, npy

    Parameters
    ----------
    filepath : str
        Filepath to image
    device : torch.device, optional
        Device on which the output tensor will be allocated.
    dtype : torch.dtype, optional
        Desired output data type. Default is `torch.float32`.
    
    Returns
    -------
    Image as a PyTorch tensor (RGB, not BGR; probably RGGB if raw)

    See also
    --------
    vim.load_image
    vtaux.get_device
    """

    return numpy2torch(vim.load_image(filepath), device, dtype)

#%% CHANNELS MANAGEMENT

def image_info(image: Union[np.ndarray, torch.Tensor]):
    shape = image.shape
    if len(shape) == 3:
        if isinstance(image, torch.Tensor):
            C, H, W = shape
        elif isinstance(image, np.ndarray):
            H, W, C = shape
        else:
            raise NotImplementedError("Expected torch.Tensor or np.ndarray")
    elif len(shape) == 2:
        H, W = shape
        C = 1
    else:
        raise NotImplementedError(
            "Image shape is {shape}. It expected image with shape (H,W), (C,H,W) or (H,W,C)"
        )

    return C, H, W

def stack_dtype(var):
    """Given a list of tensors, stack them along the first dimension and return a tensor.

    Credits to Marco Aversa, 2024.

    Parameters
    ----------
    var: list
        List of Torch tensors (torch.Tensor) or Numpy arrays (np.ndarray)

      
    Returns
    -------
    A tensor of shape (batch_size, seq_len, num_layers, hidden_size)
    """
    
    if isinstance(var[0], torch.Tensor):
        return torch.stack(var)
    elif isinstance(var[0], np.ndarray):
        return np.stack(var, axis=2)
    else:
        raise NotImplementedError("Expected torch.Tensor or np.ndarray")

def mosaic2multichannel(mosaic: Union[np.ndarray, torch.Tensor], k_H : int=2, k_W : int=2):
    """Split a spectral camera mosaic into a multi-channel image.

    Credits to Marco Aversa, 2024.

    Parameters
    ----------
    mosaic : np.ndarray, torch.Tensor
        Spectral mosaic, shape: (H,W)
    k_H, k_W : int, int, optional
        Spectral mosaic's kernel sizes. Default Bayer kernels (k_H, k_W) = (2,2).

    Returns
    -------
    imgs : np.ndarray, torch.Tensor
        Images with different wavelengths splitted in channels.
        Shape: (C, H//k_H, W//k_W) if type == torch.Tensor
        Shape: (H//k_H, W//k_W, C) if type == np.ndarray

    """

    C, H, W = image_info(mosaic)
    if C == 1:
        mosaic = mosaic.squeeze()

    x_max = k_H * (H // k_H)  # integer number of patterns
    y_max = k_W * (W // k_W)

    mosaic = mosaic[0:x_max, 0:y_max]
    all_images = [
        mosaic[i::k_H, j::k_W] for i in range(k_H) for j in range(k_W)
    ]  # some list comprehension will save us here ...

    images = stack_dtype(all_images)

    return images


def multichannel2mosaic(imgs: Union[np.ndarray, torch.Tensor], k_H : int=2, k_W : int=2):
    """Return multi-channel image to the spectral camera mosaic.

    Based on Marco Aversa's, 2024.

    Parameters
    ----------
    imgs : np.ndarray, torch.Tensor
        Images with different wavelengths splitted in channels.
        Shape: (C, H//k_H, W//k_W) if type == torch.Tensor
        Shape: (H//k_H, W//k_W, C) if type == np.ndarray
    k_H, k_W : int, int, optional
        Spectral mosaic's kernel sizes. Default Bayer kernels (k_H, k_W) = (2,2).

    Returns
    -------
    mosaic : np.ndarray, torch.Tensor
        Spectral mosaic, shape: (H,W)
    """

    C, H, W = image_info(imgs)

    if isinstance(imgs, torch.Tensor):
        mosaic = torch.zeros((H * k_H, W * k_W))
        imgs = [imgs[c] for c in range(C)]
    elif isinstance(imgs, np.ndarray):
        mosaic = np.zeros((H * k_H, W * k_W))
        imgs = [imgs[:, :, c] for c in range(C)]
    else:
        raise NotImplementedError("Expected torch.Tensor or np.ndarray")

    c = 0
    for i in range(k_H):
        for j in range(k_W):
            mosaic[i::k_H, j::k_W] = imgs[c]
            c += 1

    return mosaic

class SpectralImagesConverter:
    """Manages conversion between multi-channel and mosaic format of spectral images"""

    def __init__(self, k_H:int=2, k_W:int=2):
        
        self.is_mosaic = True
        self.k_H = k_H
        self.k_W = k_W

        # Spectral mosaic's kernel sizes, shape: (k_W, k_W)
        # Indicates number of wavelengths in the mosaic pattern (n_row, n_column)
        # For the default RGGB pattern, default Bayer kernel [2,2]
        # For a grey image the pattern should be [1,1]

    def mosaic2multichannel(self, mosaic: Union[np.ndarray, torch.Tensor]):
        
        result = mosaic2multichannel(mosaic, self.k_H, self.k_W)
        self.is_mosaic = False
        return result

    def multichannel2mosaic(self, imgs: Union[np.ndarray, torch.Tensor]):

        result = multichannel2mosaic(imgs, self.k_H, self.k_W)
        self.is_mosaic = True
        return result
    
    # def plot_image(self, image, title=None, dark=True, colormap="viridis",
    #                figsize=(2.66, 1.7), dpi=200, ax=None):
        
    #     image = image.cpu()
    #     if image.ndim > 2: 
    #         image = self.from_multichannel_to_mosaic(image)

    #     plot_image(image, title=title, dark=dark, colormap=colormap,
    #                figsize=figsize, ax=ax, dpi=dpi)

#%% IMAGE TILING / PATCHING

def image2tiles(image: Union[np.ndarray, torch.Tensor], 
                p_H : int, p_W : int, view_as_patches: bool = False):
    """Patch an image into non-overlapping tiles.

    Based on Marco Aversa's, 2024.

    Parameters
    ----------
    image : np.ndaray, torch.Tensor
        Image to tile. Image should be 2D.
    p_H, p_W : int, int
        Tile size.
    view_as_patches:
        Example for 2D image:
            If set True -> return the final output is 3D (N_patch, Patch_size_x, Patch_size_y)
                image.shape = (100,100), patch_size = (2,2) -> patches.shape = (2500,2,2)
            If set False -> return the final output is 4D (N_patch_x, N_patch_y, Patch_size_x, Patch_size_y)
                image.shape = (100,100), patch_size = (2,2) -> patches.shape = (50,50,2,2)
                
    Returns
    -------
    patches : np.ndaray, torch.Tensor
        Image splitted in overlapping patches.
    (H, W) : int, int
        Image dimensions covered in tiles.
    (N, M) : int, int
        Number of tiles alongside height and width of the covered image.
    """

    C, H, W = image_info(image)
    mosaic = C==1

    N = H // p_H
    M = W // p_W
    
    H = p_H * N  # integer number for patches
    W = p_W * M

    image = image[..., 0:H, 0:W]

    if mosaic:
        patches = image.reshape(N, p_H, M, p_W).swapaxes(1, 2)
        if view_as_patches:
            patches = patches.reshape(-1, p_H, p_W) # (N*M, p_H, p_W)
        # else: (N, M, p_H, p_W)
    else:
        if isinstance(image, np.ndarray):
            image = image.swapaxes(0, 1) # From (H, W, C) to (C, H, W)
        patches = image.reshape(C, N, p_H, M, p_W)
        patches = patches.swapaxes(2,3).swapaxes(0,1).swapaxes(1,2) # (N, M, C, p_H, p_W)
        if view_as_patches:
            patches = patches.reshape(-1, C, p_H, p_W) # (N*M, C, p_H, p_W)
            if isinstance(image, np.ndarray):
                patches = patches.swapaxes(1,2).swapaxes(2,3) # (N*M, p_H, p_W, C)
            # else: (N*M, C, p_H, p_W)
        else:
            if isinstance(image, np.ndarray):
                patches = patches.swapaxes(2,3).swapaxes(3,4) # (N, M, p_H, p_W, C)
            # else: (N, M, C, p_H, p_W)

    return patches, (H, W), (M, M)
        

def tiles2image(patches: Union[np.ndarray, torch.Tensor], H: int, W: int, mosaic: bool=False):
    """Make an image from non-overlapping tiles.

    Based on Marco Aversa's, 2024.

    Parameters
    ----------
    patches : np.ndarray, torch.Tensor
        Tiles to reconstruct the image from
    H, W : int, int
        Patched image's dimensions
    mosaic : bool, optional
        Whether tiles are in mosaic format (h, w) or multi-channel format instead (4, h/2, w/2). 
        Default is False.
    
    Returns
    -------
    image : np.ndarray, torch.Tensor
        Image reconstructed from tiles, in mosaic format if patches are in mosaic format 
        (same dtype as input)
    """

    ndims = patches.ndim

    if ndims == 3:
        view_as_patches = True
        T, p_H, p_W = patches.shape
        N = int(H/p_H)
        M = int(W/p_W)
        if N*M != T:
            raise ValueError("Array dimensions could not be recovered from patch dimensions")
    elif ndims == 4 and mosaic:
        view_as_patches = False
        N, M, p_H, p_W = patches.shape
    elif not mosaic:
        view_as_patches = True
        if isinstance(patches, torch.Tensor):
            T, C, p_H, p_W = patches.shape
        else:
            T, p_H, p_W, C = patches.shape
            patches = patches.swapaxes(2, 3).swapaxes(1, 2)
        N = int(H/p_H)
        M = int(W/p_W)
        if N*M != T:
            raise ValueError("Array dimensions could not be recovered from patch dimensions")
    elif ndims == 5:
        view_as_patches = False
        N, M, C, p_H, p_W = patches.shape
        if isinstance(patches, torch.Tensor):
            N, M, C, p_H, p_W = patches.shape
        else:
            N, M, p_H, p_W, C = patches.shape
            patches = patches.swapaxes(3, 4).swapaxes(3, 2)
    else:
        raise ValueError("Patches array must have between 3 and 5 dimensions")
    if mosaic: C=1
    
    if H!=N*p_H or W!=M*p_W:
        raise ValueError("Covered image dimensions are not multiples of patch dimensions")

    if mosaic: 
        if view_as_patches:
            patches = patches.reshape(N, M, p_H, p_W) # From (N*M, p_H, p_W)
        return patches.swapaxes(1, 2).reshape(H, W) # From (N, M, p_H, p_W)
    else:
        if view_as_patches:
            patches = patches.reshape(N, M, C, p_H, p_W) # From (N*M, p_H, p_W)
        patches = patches.swapaxes(1,2).swapaxes(0,1) # (C, N, M, p_H, p_W)
        patches = patches.swapaxes(2,3) # (C, N, p_H, M, p_W)
        patches = patches.reshape(C, H, W)
        if isinstance(patches, np.ndarray):
            patches = patches.swapaxes(0, 1).swapaxes(1,2) # (H, W, C)
        return patches
    

def image2patches(image: Union[np.ndarray, torch.Tensor], p_H : int, p_W : int, 
                  overlapping_factor=.5, view_as_patches: bool = False, debug=False):
    """Patch a 2D image into overlapping patches.

    Based on Marco Aversa's, 2024.

    Parameters
    ----------
    image : np.ndaray, torch.Tensor
        Image to patch. Image should be 2D.
    p_H, p_W : int, int
        Tile size.
    overlapping_factor : float
        Desired overlapped fraction of each tile. If a tuple of length 2 is provided, 
        then first element will be height overlap, second will be width overlap.
    view_as_patches : bool
        Example for 2D image:
            If set True -> return the final output is 3D (N_patch, Patch_size_x, Patch_size_y)
                image.shape = (100,100), patch_size = (2,2) -> patches.shape = (2500,2,2)
            If set False -> return the final output is 4D (N_patch_x, N_patch_y, Patch_size_x, Patch_size_y)
                image.shape = (100,100), patch_size = (2,2) -> patches.shape = (50,50,2,2)

    Returns
    -------
    patches : np.ndaray, torch.Tensor
        Image splitted in overlapping patches.
    (H, W) : int, int
        Image dimensions covered in tiles.
    (N, M) : int, int
        Number of tiles alongside height and width of the covered image.
    """

    C, H, W = image_info(image)
    mosaic = C==1
    if not mosaic and isinstance(image, np.ndarray):
        image = image.swapaxes(1,2).swapaxes(0,1) # (C,H,W) instead of (H,W,C)
    vtaux.print_debug("Original image", H, "x", W, debug=debug)
    
    if isinstance(overlapping_factor, tuple):
        if len(overlapping_factor)!=2:
            raise ValueError("Overlapping factor should be either a number from 0 to 1, or a tuple of length 2.")
        ov0 = int(np.round(overlapping_factor[0]*p_H/2))
        ov1 = int(np.round(overlapping_factor[1]*p_W/2))
    else:
        ov0 = int(np.round(overlapping_factor*p_H/2))
        ov1 = int(np.round(overlapping_factor*p_W/2))

    vtaux.print_debug("Overlapping pixels on each side", ov0, ov1, debug=debug)
    patches = []
    i = 0; N = 0
    while i+p_H <= H:
        j = 0; M = 0
        while j+p_W <= W:
            patches.append(image[..., i:i+p_H, j:j+p_W])
            j += p_W - ov1; M += 1
        i += p_H - ov0; N += 1
    vtaux.print_debug("Number of patches", N, M, debug=debug)
    H = i + ov0
    W = j + ov1
    vtaux.print_debug("Covered image", H, "x", W, debug=debug)
    
    if isinstance(image, np.ndarray):
        patches = np.array(patches)
    else:
        patches = torch.stack(patches, dim=0)
    vtaux.print_debug("Patches array shape", patches.shape, debug=debug)

    if view_as_patches:
        if not mosaic and isinstance(image, np.ndarray):
            patches = patches.swapaxes(1,2).swapaxes(2,3) # (N*M, p_H, p_W, C)
        # else: (N*M, C, p_H, p_W)
    else:
        if mosaic:
            patches = patches.reshape(N, M, p_H, p_W)
        else:
            patches = patches.reshape(N, M, C, p_H, p_W)
            if isinstance(image, np.ndarray):
                patches = patches.swapaxes(2,3).swapaxes(3,4)  # (N, M, p_H, p_W, C)
            # else: (N, M, C, p_H, p_W)
    
    return patches, (H, W), (N, M)
        

def patches2image(patches: Union[np.ndarray, torch.Tensor], 
                  H: int, W: int, N: int, M: int, 
                  mosaic: bool=False, overlapping_factor=.5, debug=False):
    """Make a 2D image from overlapping patches.

    Parameters
    ----------
    patches : np.ndarray, torch.Tensor
        Patches
    H, W : int
        Dimensions of the patched image to be recovered
    N, M : int
        Number of patches alongside the height and the width of the image
    mosaic : bool, optional
        Whether the patches and final image are in mosaic format (H, W) or in 
        multi-channel format (C, H, W)
    overlapping_factor : float, optional
        Desired overlapped fraction of each tile. If a tuple of length 2 is provided, 
        then first element will be height overlap, second will be width overlap. 
        Default is 0.5.

    Returns
    -------
    image : np.ndaray, torch.Tensor
        Image reconstructed from patches (same dtype as input)
    """

    ndims = patches.ndim

    if ndims == 3:
        view_as_patches = True
        T, p_H, p_W = patches.shape
        if N*M != T:
            raise ValueError("Array dimensions could not be recovered from patch dimensions")
    elif ndims == 4 and mosaic:
        view_as_patches = False
        n, m, p_H, p_W = patches.shape
        T = n*m
        if n!=N or m!=M:
            raise ValueError("Dimensions mismatch found between patches and input parameters")
    elif not mosaic:
        view_as_patches = True
        if isinstance(patches, torch.Tensor):
            T, C, p_H, p_W = patches.shape
        else:
            T, p_H, p_W, C = patches.shape
            patches = patches.swapaxes(2, 3).swapaxes(1, 2)
    elif ndims == 5:
        view_as_patches = False
        if isinstance(patches, torch.Tensor):
            n, m, C, p_H, p_W = patches.shape
        else:
            n, m, p_H, p_W, C = patches.shape
            patches = patches.swapaxes(3, 4).swapaxes(3, 2)
        if n!=N or m!=M:
            raise ValueError("Dimensions mismatch found between patches and input parameters")
        T = n*m
    else:
        raise ValueError("Patches array must have between 3 and 5 dimensions")
    if mosaic: C=1

    if not view_as_patches:
        patches = patches.reshape(T, *patches.shape[2:])
    patches = patches.cpu()

    if isinstance(overlapping_factor, tuple):
        if len(overlapping_factor)!=2:
            raise ValueError("Overlapping factor should be either a number from 0 to 1, or a tuple of length 2.")
        ov0 = int(np.round(overlapping_factor[0]*p_H/2))
        ov1 = int(np.round(overlapping_factor[1]*p_W/2))
    else:
        ov0 = int(np.round(overlapping_factor*p_H/2))
        ov1 = int(np.round(overlapping_factor*p_W/2))    
    vtaux.print_debug("Overlapping pixels on each side", ov0, ov1, debug=debug)

    if isinstance(patches, np.ndarray):
        if mosaic: image = np.zeros((H, W)).astype(np.float32)
        else: image = np.zeros((C, H, W)).astype(np.float32)
    else:
        if mosaic: image = torch.zeros((H, W)).type(torch.float32)
        else: image = torch.zeros((C, H, W)).type(torch.float32)

    k = 0
    i = 0; n = 0
    while i+p_H <= H:
        j = 0; m = 0
        while j+p_W <= W:
            if i!=H-p_H:
                patches[k][..., p_H-ov0:, :] = patches[k][..., p_H-ov0:, :]/2
            if j!=W-p_W:
                patches[k][..., :, p_W-ov1:] = patches[k][..., :, p_W-ov1:]/2
            if i!=0:
                patches[k][..., :ov0, :] = patches[k][..., :ov0, :]/2
            if j!=0:
                patches[k][..., :, :ov1] = patches[k][..., :, :ov1]/2
            image[..., i:i+p_H, j:j+p_W] += patches[k]; k += 1
            j += p_W - ov1; m += 1
        i += p_H - ov0; n += 1
    new_H, new_W = (i+ov0, j+ov1)
    vtaux.print_debug("Number of patches considered", n, m, debug=debug)
    vtaux.print_debug("Image covered", new_H, "x", new_W, debug=debug)

    if isinstance(patches, np.ndarray):
        if mosaic: image = image.astype(patches.dtype)
        else: image = image.astype(patches.dtype).swapaxes(0,1).swapaxes(1,2)
    else:
        image = image.type(patches.dtype)

    return image


#%% IMAGE ANALYSIS

def MSE(image_1, image_2):
    """Mean-Square Error (MSE) to compare two images"""
    
    if isinstance(image_1, torch.Tensor):
        image_1 = image_1.type(torch.float32).cpu()
        image_2 = image_2.type(torch.float32).cpu()
        mse = torch.mean( ( image_1 - image_2 )**2 )
    else:
        image_1, image_2 = np.asarray(image_1), np.asarray(image_2)
        image_1 = image_1.astype(np.float32)
        image_2 = image_2.astype(np.float32)
        mse = np.mean( ( image_1 - image_2 )**2 )
    
    return mse

def PSNR(image_1, image_2, byte_depth=8):
    """Peak Signal-to-Noise Ratio (PSNR) to compare two images.

    Parameters
    ----------
    image_1, image_2 : np.array
        The two pictures to compare. Must have the same shape.
    byte_depth : int, optional
        Image byte depth. Default is 8 for 8-bit images.
        
    Returns
    -------
    psnr : float
    """
    
    mse = MSE(image_1, image_2)

    if(mse == 0):  return np.inf
    # If MSE is null, then the two pictures are equal

    maximum_pixel = 2**byte_depth - 1

    psnr = 20 * log10(maximum_pixel / sqrt(mse)) # dB

    return psnr

def SSIM(image_1, image_2, byte_depth=8, win_size=None):
    
    """Structural Similarity Index Measure (SSIM) to compare two images.
    
    Parameters
    ----------
    image_1, image_2 : np.array
        The two images to compare. Must have the same shape.
    byte_depth : int, optional
        Image byte depth. Default is 8 for 8-bit images. Default is 8.
    win_size : 
        Skimage's parameter. Default is None.
        
    Returns
    -------
    ssim : float
    
    See also
    --------
    skimage.metrics.structural_similarity
    """
     
    data_range = 2**byte_depth

    if isinstance(image_1, torch.Tensor): # assumed (C, H, W) instead of (H, W, C)
        image_1 = image_1.cpu().numpy()
        image_2 = image_2.cpu().numpy()
    else:
        image_1, image_2 = np.asarray(image_1), np.asarray(image_2)
    
    return structural_similarity(image_1, image_2, 
                                 data_range=data_range, win_size=win_size)

def IOU(mask_1, mask_2):
    """Intersection Over Union (IOU) to compare two boolean masks.
    
    Parameters
    ----------
    mask_1, mask_2 : np.array, torch.Tensor
        The two image masks to compare. Must have the same shape.
        
    Returns
    -------
    iou : float
    """

    if type(mask_1) is not np.ndarray:
        intersection_count = int( torch.sum(torch.logical_and(mask_1, mask_2)) )
        union_count = int( torch.sum(torch.logical_or(mask_1, mask_2)) )
    else:
        intersection_count = int( np.sum(np.logical_and(mask_1, mask_2)) )
        union_count = int( np.sum(np.logical_or(mask_1, mask_2)) )
    return intersection_count / union_count