import numpy as np

from peskit.common.constant import S2PI, TINY


def gaussian_kernel(
    x,
    resolution=1.0,
):
    """Return a 1-dimensional Gaussian function.

    gaussian(x, amplitude, center, sigma) =
        (amplitude/(S2PI*sigma)) * exp(-(1.0*x-center)**2 / (2*sigma**2))

    """
    amplitude = 1.0
    center = x.mean()
    return (amplitude / (max(TINY, S2PI * resolution))) * np.exp(
        -((1.0 * x - center) ** 2) / max(TINY, (2 * resolution**2))
    )
