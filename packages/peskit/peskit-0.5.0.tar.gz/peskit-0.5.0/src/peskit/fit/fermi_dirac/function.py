import numpy as np
import numpy.typing as npt

from peskit.common.constant import CONST_KB
from peskit.common.function import do_convolve


def fermi_dirac(
    x: np.ndarray,
    center: float,
    temp: float,
) -> np.ndarray:
    return 1.0 / (1.0 + np.exp((1.0 * x - center) / (temp * CONST_KB)))


def fermi_dirac_linbkg(
    x: np.ndarray,
    center: float,
    temp: float,
    back0: float,
    back1: float,
    dos0: float,
    dos1: float,
) -> np.ndarray:
    """Fermi-dirac edge with linear backgrounds above and below the fermi level.

    Note
    ----
    `back0` and `back1` corresponds to the linear background above and below EF (due to
    non-homogeneous detector efficiency or residual intensity on the phosphor screen
    during sweep mode), while `dos0` and `dos1` corresponds to the linear density of
    states below EF including the linear background.
    """
    return (back0 + back1 * x) + (dos0 - back0 + (dos1 - back1) * x) / (
        1 + np.exp((1.0 * x - center) / (temp * CONST_KB))
    )


def fermi_dirac_linbkg_broad(
    x: npt.NDArray[np.float64],
    center: float,
    temp: float,
    resolution: float,
    back0: float,
    back1: float,
    dos0: float,
    dos1: float,
) -> npt.NDArray[np.float64]:
    """Resolution-broadened Fermi edge with linear backgrounds above and below EF."""
    return do_convolve(
        x,
        fermi_dirac_linbkg,
        resolution=resolution,
        center=center,
        temp=temp,
        back0=back0,
        back1=back1,
        dos0=dos0,
        dos1=dos1,
    )
