import numpy as np

from peskit.common.distribution import bose_einstein, fermi_dirac
from peskit.common.function import do_convolve


def test_do_convolve():
    x = np.linspace(-1, 1, 100, dtype=np.float64)

    def func(x):
        return np.exp(-(x**2))

    resolution = 1.0
    result = do_convolve(x, func, resolution)
    assert result is not None
    assert isinstance(result, np.ndarray)
    assert np.all(result > 0)


def test_bose_einstein():
    z = np.linspace(0, 1, 100, dtype=np.float64)
    temp = 300.0
    result = bose_einstein(z, temp)
    assert result is not None
    assert isinstance(result, np.ndarray)
    assert np.all(result > 0)


def test_fermi_dirac():
    z = np.linspace(-1, 1, 100, dtype=np.float64)
    temp = 300.0
    result = fermi_dirac(z, temp)
    assert result is not None
    assert isinstance(result, np.ndarray)
    assert np.all(result > 0)
