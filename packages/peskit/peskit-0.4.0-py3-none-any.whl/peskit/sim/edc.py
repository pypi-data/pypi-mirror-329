import numpy as np
import xarray as xr

from peskit.common.distribution import fermi_dirac
from peskit.common.function import convolve
from peskit.fit.broadening.function import gaussian_kernel


def get_edc() -> xr.DataArray:
    x = np.linspace(-0.1, 0.01, 200)
    self_energy = 0.05 * x - 1j * 0.05 * x**2 - 1j * 0.01
    bare_band = -0.03
    matrix_element = 2.0
    greens_function = 1 / (x - bare_band - self_energy)
    spectral_function = -1 / np.pi * np.imag(greens_function)
    data = matrix_element * spectral_function * fermi_dirac(x, 20.0)
    # data = matrix_element * spectral_function
    data = convolve(gaussian_kernel(resolution=1e-3, x=x), data)
    # data = gaussian_filter1d(data, sigma=10.0)
    # data = add_noise(data, int(1e5))
    return xr.DataArray(data, coords=[x], dims=["eV"])
