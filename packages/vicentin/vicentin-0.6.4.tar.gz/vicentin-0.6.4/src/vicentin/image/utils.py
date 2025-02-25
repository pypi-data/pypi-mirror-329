import numpy as np
from scipy.signal import convolve2d
from scipy.ndimage import gaussian_filter as scipy_gaussian_filter

import jax
from jax.scipy.signal import convolve2d as jax_convolve2d

# from jax.scipy.ndimage import gaussian_filter as jax_gaussian_filter

from vicentin.utils import _wrap_func, asarray, sum, log10, sqrt, repeat, arange


convolve = _wrap_func(convolve2d, jax_convolve2d)
gaussian_filter = _wrap_func(scipy_gaussian_filter, scipy_gaussian_filter)


def _img2blocks_numpy(img, block_shape, step_row, step_col):
    """
    Extracts non-overlapping or overlapping blocks from an image using NumPy (CPU).

    Args:
        img (np.ndarray): Input image.
        block_shape (tuple): Block size (height, width).
        step_row (int): Step size in row direction.
        step_col (int): Step size in column direction.

    Returns:
        np.ndarray: Extracted blocks.
    """

    img = asarray(img)  # Converts input to either np or jnp
    H, W = img.shape
    bH, bW = block_shape

    n_rows = (H - bH) // step_row + 1
    n_cols = (W - bW) // step_col + 1

    new_shape = (n_rows, n_cols, bH, bW)
    new_strides = (
        img.strides[0] * step_row,
        img.strides[1] * step_col,
        img.strides[0],
        img.strides[1],
    )
    blocks = np.lib.stride_tricks.as_strided(img, shape=new_shape, strides=new_strides, writeable=False)
    return blocks.copy()


def _img2blocks_jax(img, block_shape, step_row, step_col):
    """
    Extracts non-overlapping or overlapping blocks from an image using JAX (GPU/TPU).

    Args:
        img (jnp.ndarray): Input image.
        block_shape (tuple): Block size (height, width).
        step_row (int): Step size in row direction.
        step_col (int): Step size in column direction.

    Returns:
        jnp.ndarray: Extracted blocks.
    """

    img = asarray(img)
    H, W = img.shape
    bH, bW = block_shape

    n_rows = (H - bH) // step_row + 1
    n_cols = (W - bW) // step_col + 1

    row_idx = arange(0, H - bH + 1, step_row).reshape(-1, 1)
    col_idx = arange(0, W - bW + 1, step_col).reshape(1, -1)

    row_idx = repeat(row_idx, n_cols, axis=1).flatten()
    col_idx = repeat(col_idx, n_rows, axis=0).flatten()

    blocks = jax.vmap(lambda r, c: jax.lax.dynamic_slice(img, (r, c), (bH, bW)))(row_idx, col_idx)
    return blocks.reshape(n_rows, n_cols, bH, bW)


def img2blocks(img, block_shape, step_row=-1, step_col=-1):
    """
    Extracts non-overlapping or overlapping blocks from an image.

    Args:
        img (np.ndarray or jnp.ndarray): Input image.
        block_shape (tuple): Block size (height, width).
        step_row (int, optional): Step size in row direction. Defaults to block height.
        step_col (int, optional): Step size in column direction. Defaults to block width.

    Returns:
        np.ndarray or jnp.ndarray: Extracted blocks.
    """

    if step_row == -1:
        step_row = block_shape[0]
    if step_col == -1:
        step_col = block_shape[1]

    return _wrap_func(_img2blocks_numpy, _img2blocks_jax)(img, block_shape, step_row, step_col)


def PSNR(img1, img2):
    """
    Compute the Peak Signal-to-Noise Ratio (PSNR) between two images.

    PSNR is defined as:
        PSNR = 20 * log10(max_I / sqrt(MSE))
    where MSE (Mean Squared Error) is computed between img1 and img2, and max_I is the
    maximum possible pixel value (assumed here as the maximum value in img1).

    Parameters
    ----------
    img1 : numpy.ndarray or jax.numpy.ndarray
        The first image.
    img2 : numpy.ndarray or jax.numpy.ndarray
        The second image. Must have the same shape as img1.

    Returns
    -------
    float
        The PSNR value in decibels (dB).

    Raises
    ------
    AssertionError
        If the input images do not have the same shape.
    """
    assert img1.shape == img2.shape, "Images must have the same dimensions."
    H, W = img1.shape[:2]

    mse = sum((img1 - img2) ** 2) / (H * W)
    max_I = img1.max()
    return 20 * log10(max_I / sqrt(mse))


def get_neighbors(H, W, L, row, col, k, neighborhood=4):
    """
    Retrieves the neighboring pixels of a given pixel in a 1D, 2D, or 3D image.

    This function determines valid neighboring coordinates based on the specified
    neighborhood type (4-neighborhood or 8-neighborhood). The neighbors are constrained
    within the image dimensions to avoid out-of-bounds errors.

    Args:
        H (int): The height (number of rows) of the image.
        W (int): The width (number of columns) of the image.
        L (int): The depth (number of channels) of the image.
        row (int): The row index of the current pixel.
        col (int): The column index of the current pixel.
        k (int): The depth index of the current pixel.
        neighborhood (int, optional): The type of neighborhood to consider:
            - `4`: Only direct neighbors (left, right, up, down, front, back).
            - `8`: Includes diagonal neighbors as well.
            Defaults to `4`.

    Returns:
        list[tuple[int, int, int]]: A list of tuples representing valid neighboring coordinates.

    Time Complexity:
        - O(1), as it evaluates a constant number of neighbor positions.

    Space Complexity:
        - O(1), as it only stores a small list of neighbors.

    Raises:
        ValueError: If `neighborhood` is not 4 or 8.
    """
    neighbors = []
    possible_moves = []

    if neighborhood == 4:
        possible_moves = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]
    elif neighborhood == 8:
        possible_moves = [(i, j, m) for i in [-1, 0, 1] for j in [-1, 0, 1] for m in [-1, 0, 1] if not (i == j == m == 0)]

    for di, dj, dm in possible_moves:
        ni, nj, nm = row + di, col + dj, k + dm
        if 0 <= ni < H and 0 <= nj < W and 0 <= nm < L:
            neighbors.append((ni, nj, nm))

    return neighbors
