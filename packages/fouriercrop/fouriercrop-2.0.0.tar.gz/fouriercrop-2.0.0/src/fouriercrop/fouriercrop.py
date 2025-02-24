"""Main module."""

from functools import partial
from pathlib import Path
from typing import Tuple, Union

import mrcfile
import numpy as np
import torch


def load_mrc(
    load_path: Union[str, Path],
    as_tensor: bool = False,
    get_voxel_size: bool = False,
) -> Union[np.ndarray, torch.Tensor, Tuple[Union[np.ndarray, torch.Tensor], np.ndarray]]:
    """Loads data from an MRC file and optionally retrieves voxel size.

    Args:
        load_path (Union[str, Path]): Path to the MRC file.
        as_tensor (bool, optional): If True, returns tensor (default=False).
        get_voxel_size (bool, optional): If True, returns voxel size (default=False).

    Returns:
        Tuple[Union[np.ndarray, torch.Tensor], np.ndarray]: The MRC data and voxel size.

    Raises:
        FileNotFoundError: If the input file does not exist.
    """
    if not Path(load_path).is_file():
        raise FileNotFoundError(f"Error! {load_path} does not exist.")

    with mrcfile.open(load_path, permissive=True) as mrc:
        voxel_size = np.array(
            [mrc.voxel_size.z, mrc.voxel_size.y, mrc.voxel_size.x], dtype=np.float32
        )
        data = mrc.data

    data = torch.from_numpy(data) if as_tensor else data

    return (data, voxel_size) if get_voxel_size else data


def save_mrc(
    save_path: Union[str, Path],
    save_data: Union[np.ndarray, torch.Tensor],
    voxel_size: float = 1.0,
) -> None:
    """Saves data to an MRC file.

    Args:
        save_path (Union[str, Path]): Path to save the MRC file.
        save_data (Union[np.ndarray, torch.Tensor]): Data to save.
        voxel_size (float, optional): Voxel size of the data (default=1.0).
    """
    if isinstance(save_data, torch.Tensor):
        save_data = save_data.detach().cpu().numpy()

    with mrcfile.new(save_path, overwrite=True) as mrc:
        mrc.set_data(save_data)
        mrc.voxel_size = (voxel_size,) * 3


class FourierCrop:
    """Enables downsampling and other operations based on Fourier domain cropping.

    It supports 2D tensors in the BCHW format and 3D tensors in the BCDHW format.
    """

    def __init__(
        self,
        pad_mode: int = 0,
        dim: Tuple = (-3, -2, -1),
        epsilon: float = 1e-6,
    ) -> None:
        """Initializes with specified padding mode, dimensions, and epsilon value.

        Args:
            pad_mode (int, optional): Determines the cropping function to use.
            dim (Tuple, optional):
                Dimensions over which to perform operations (default=(-3, -2, -1)).
            epsilon (float, optional):
                Small value to avoid division by zero (default=1e-6).
        """
        super().__init__()
        self.crop_func = {
            0: self.crop_center,
            1: self.pad_center,
            2: self.crop_center_pad,
        }[pad_mode]
        self.norm_func = partial(self.norm, dim=dim, epsilon=epsilon)
        self.fft_func = partial(self.fft, dim=dim)
        self.ifft_func = partial(self.ifft, dim=dim)

    @staticmethod
    def crop_center(x: torch.Tensor, bin_factor: int = 2) -> torch.Tensor:
        """Crops the central region of a tensor based on a specified bin_factor factor.

        Args:
            x (torch.Tensor):
                Input 2D tensors in the BCHW format or 3D tensors in the BCDHW format.
            bin_factor (int, optional):
                Factor determining the size of the cropped region (default=2).

        Returns:
            torch.Tensor: Cropped tensor.
        """
        input_shape = x.shape[2:]
        if len(input_shape) not in [2, 3]:
            raise ValueError("Unsupported dimension. Supported values are 2 or 3.")

        input_center = [s // 2 for s in input_shape]
        target_center = [s // (2 * bin_factor) for s in input_shape]
        crop_slice = tuple(slice(i - t, i + t) for i, t in zip(input_center, target_center))

        return x[(..., *crop_slice)]

    @staticmethod
    def crop_center_pad(x: torch.Tensor, bin_factor: int = 2) -> torch.Tensor:
        """Crops the central region of a tensor and pads it back to its original size.

        Args:
            x (torch.Tensor):
                Input 2D tensors in the BCHW format or 3D tensors in the BCDHW format.
            bin_factor (int, optional):
                Factor determining the size of the cropped region (default=2).

        Returns:
            torch.Tensor: Cropped and padded tensor.
        """
        x_pad = torch.zeros_like(x)
        x_crop = FourierCrop.crop_center(x, bin_factor=bin_factor)

        input_shape = x_pad.shape[2:]
        input_center = [s // 2 for s in input_shape]
        target_center = [s // (2 * bin_factor) for s in input_shape]
        crop_slice = tuple(slice(i - t, i + t) for i, t in zip(input_center, target_center))

        x_pad[(..., *crop_slice)] = x_crop
        return x_pad

    @staticmethod
    def pad_center(x: torch.Tensor, bin_factor: int = 2) -> torch.Tensor:
        """Centers the original tensor within the new padded tensor."""
        pad_shape = [s * 2 for s in x.shape[2:]]
        pad_shape = list(x.shape[:2]) + pad_shape
        x_pad = torch.zeros(pad_shape, dtype=x.dtype, device=x.device)

        input_shape = x_pad.shape[2:]
        input_center = [s // 2 for s in input_shape]
        target_center = [s // (2 * bin_factor) for s in input_shape]
        crop_slice = tuple(slice(i - t, i + t) for i, t in zip(input_center, target_center))
        x_pad[(..., *crop_slice)] = x
        return x_pad

    @staticmethod
    def norm(x: torch.Tensor, dim: Tuple = (-3, -2, -1), epsilon: float = 1e-6) -> torch.Tensor:
        """Normalizes a tensor by its mean and standard deviation."""
        mean = x.mean(dim=dim, keepdim=True)
        std = x.std(dim=dim, keepdim=True)
        return (x - mean) / (std + epsilon)

    @staticmethod
    def fft(x: torch.Tensor, dim: Tuple = (-3, -2, -1), norm: str = "ortho") -> torch.Tensor:
        """Applies 3D Fast Fourier Transform (FFT) to input data."""
        return torch.fft.fftshift(torch.fft.fftn(x, dim=dim, norm=norm), dim=dim)

    @staticmethod
    def ifft(x: torch.Tensor, dim: Tuple = (-3, -2, -1), norm: str = "ortho") -> torch.Tensor:
        """Applies Inverse Fast Fourier Transform (IFFT) to input data."""
        return torch.fft.ifftn(torch.fft.ifftshift(x, dim=dim), dim=dim, norm=norm)

    def __call__(
        self,
        x: torch.Tensor,
        bin_factor: int = 2,
        norm_flag: bool = False,
    ) -> torch.Tensor:
        """Applies Fourier transform, crop, and inverse transform."""
        if norm_flag:
            x = self.norm_func(x)
            x = self.fft_func(x)
            x = self.crop_func(x, bin_factor)
            x = self.ifft_func(x).real
            x = self.norm_func(x)

        else:
            x = self.fft_func(x)
            x = self.crop_func(x, bin_factor)
            x = self.ifft_func(x).real
        return x
