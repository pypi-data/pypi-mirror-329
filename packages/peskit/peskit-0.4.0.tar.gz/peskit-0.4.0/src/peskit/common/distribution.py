import numba as nb
import numpy as np
import numpy.typing as npt

from .constant import CONST_KB, TINY


@nb.njit(nogil=True, cache=True)
def bose_einstein(
    z: npt.NDArray[np.float64 | np.complex128],
    temp: float,
    offset: float = 0.0,
) -> npt.NDArray[np.float64 | np.complex128]:
    """
    Calculate the Bose-Einstein distribution for a given energy array.

    Parameters
    ----------
    z : npt.NDArray[np.float64 | np.complex128]
        Array of energy values.
    temp : float
        Temperature in Kelvin.
    offset : float, optional
        Energy offset, by default 0.0.

    Returns
    -------
    npt.NDArray[np.float64 | np.complex128]
        Array of Bose-Einstein distribution values corresponding to the input energies.
    """
    x = (z - offset) / (max(TINY, temp * CONST_KB))
    # if np.where(np.atleast_1d(x.real) < 0):
    return 1.0 / (np.exp(x) - 1.0)
    # return np.exp(-x) / (1.0 - np.exp(-x))


@nb.njit(nogil=True, cache=True)
def fermi_dirac(
    z: npt.NDArray[np.float64 | np.complex128], temp: float, offset: float = 0.0
) -> npt.NDArray[np.float64 | np.complex128]:
    """
    Calculate the Fermi-Dirac distribution for a given array of energies.

    Parameters
    ----------
    z : npt.NDArray[np.float64 | np.complex128]
        Array of energy values.
    temp : float
        Temperature in Kelvin.
    offset : float, optional
        Energy offset, by default 0.0.

    Returns
    -------
    npt.NDArray[np.float64 | np.complex128]
        Array of Fermi-Dirac distribution values corresponding to the input energies.
    """
    x = (z - offset) / (max(TINY, temp * CONST_KB))
    # if np.where(np.atleast_1d(x).real < 0):
    return 1.0 / (np.exp(x) + 1.0)
    # return np.exp(-x) / (1.0 + np.exp(-x))
    # return np.exp(-x) / (1.0 + np.exp(-x))
