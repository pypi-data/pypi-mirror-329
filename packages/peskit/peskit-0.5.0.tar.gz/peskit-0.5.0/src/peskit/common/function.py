# import Callable
from collections.abc import Callable

import numba as nb
import numpy as np
import numpy.typing as npt

from peskit.common.constant import TINY

# def convolve(arr, kernel):
#     kernel = kernel / np.sum(kernel)
#     return np.convolve(arr, kernel, mode="same")


def convolve(arr, kernel):
    npts = min(arr.size, kernel.size)
    pad = np.ones(npts)
    tmp = np.concatenate((pad * arr[0], arr, pad * arr[-1]))
    out = np.convolve(tmp, kernel, mode="valid")
    noff = int((len(out) - npts) / 2)
    return out[noff : noff + npts] / np.sum(kernel)


# def convolve(arr, kernel):
#     """Simple convolution of two arrays."""
#     npts = min(arr.size, kernel.size)
#     pad = np.ones(npts)
#     tmp = np.concatenate((pad * arr[0], arr, pad * arr[-1]))
#     out = np.convolve(tmp, kernel, mode="valid")
#     noff = int((len(out) - npts) / 2)
#     return out[noff : noff + npts]


def add_noise(
    intensity: npt.NDArray[np.float64],
    count: int = int(1e5),
) -> npt.NDArray[np.float64]:
    """
    Add Poisson noise to the given intensity array.

    Parameters
    ----------
    intensity : npt.NDArray[np.float64] | npt.NDArray[np.float64, np.float64] | npt.NDArray[np.float64, np.float64, np.float64]
        The intensity array to which noise will be added. Can be a 1D, 2D, or 3D array.

    count : float, optional
        The total count to normalize the intensity to before adding noise. Default is 1e4.

    Returns
    -------
    npt.NDArray[np.float64]
        The intensity array with added Poisson noise.

    Notes
    -----
    If the intensity array contains complex numbers, it will be returned unchanged.
    """
    if np.iscomplexobj(intensity):
        return intensity
    if count is not None:
        rng = np.random.default_rng(1)
        # Normalize the intensity to sum to 1
        scaling_factor = float(count / intensity.sum())
        intensity = (
            rng.poisson(intensity * scaling_factor, size=intensity.shape)
            / scaling_factor
        )
    return intensity


def do_convolve(
    x: npt.NDArray[np.float64],
    func: Callable,
    resolution: float,
    pad: int = 3,  # 5
    **kwargs,
) -> npt.NDArray[np.float64]:
    r"""Convolves `func` with gaussian of FWHM `resolution` in `x`.

    Parameters
    ----------
    x
        A evenly spaced array specifing where to evaluate the convolution.
    func
        Function to convolve.
    resolution
        FWHM of the gaussian kernel.
    pad
        Multiples of the standard deviation :math:`\sigma` to pad with.
    **kwargs
        Additional keyword arguments to `func`.

    """
    xn, g = _gen_kernel(
        np.asarray(x, dtype=np.float64), float(resolution), pad=int(pad)
    )
    return np.convolve(func(xn, **kwargs), g, mode="valid")


@nb.njit(cache=True)
def _gen_kernel(
    x: npt.NDArray[np.float64], resolution: float, pad: int = 3
) -> tuple[npt.NDArray[np.float64], npt.NDArray[np.float64]]:
    r"""Generate a Gaussian kernel for convolution.

    Parameters
    ----------
    x
        The input array of x values.
    resolution
        The resolution of the kernel given as FWHM.
    pad
        Multiples of the standard deviation :math:`\sigma` to truncate the kernel at.

    Returns
    -------
    extended
        The domain of the kernel.
    gauss
        The gaussian kernel defined on `extended`.

    """
    delta_x = x[1] - x[0]

    sigma = abs(resolution) / np.sqrt(8 * np.log(2))  # resolution given in FWHM
    n_pad = int(sigma * pad / delta_x + 0.5)
    x_pad = n_pad * delta_x

    extended = np.linspace(x[0] - x_pad, x[-1] + x_pad, 2 * n_pad + len(x))
    gauss = np.exp(
        -(np.linspace(-x_pad, x_pad, 2 * n_pad + 1) ** 2) / max(TINY, 2 * sigma**2)
    )
    gauss /= gauss.sum()
    return extended, gauss
