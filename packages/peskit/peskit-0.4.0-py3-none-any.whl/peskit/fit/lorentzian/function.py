import numpy as np

from peskit.common.constant import TINY

# import numpy.typing as npt


def lorentzian(
    x,
    amplitude=1.0,
    center=0.0,
    sigma=1.0,
):
    """Return a 1-dimensional Lorentzian function.

    lorentzian(x, amplitude, center, sigma) =
        (amplitude/(1 + ((1.0*x-center)/sigma)**2)) / (pi*sigma)

    """
    return (amplitude / (1 + ((1.0 * x - center) / max(TINY, sigma)) ** 2)) / max(
        TINY, (np.pi * sigma)
    )


# def lorentzian(
#     x: npt.NDArray[np.complex128],
#     center_real: float,
#     center_imag: float,
#     amplitude_real: float,
# ) -> npt.NDArray[np.float64]:
#     val = x.imag - center_imag
#     val = np.where(np.abs(val) < TINY, TINY, val)
#     return (-1 / np.pi) * ((amplitude_real) / (x - center_real + 1j * val)).imag
