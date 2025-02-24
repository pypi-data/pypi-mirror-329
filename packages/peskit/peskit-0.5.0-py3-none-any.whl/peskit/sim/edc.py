import numpy as np
import xarray as xr

from peskit.common.distribution import fermi_dirac
from peskit.common.function import add_noise


def get_edc() -> xr.DataArray:
    x = np.linspace(-0.1, 0.01, 200)
    self_energy = 0.05 * x - 1j * 0.05 * x**2 - 1j * 0.01
    bare_band = -0.03
    bare_band2 = -0.01
    matrix_element = 2.0
    greens_function = 1 / (x - bare_band - self_energy)
    greens_function += 1 / (x - bare_band2 - self_energy)
    spectral_function = -1 / np.pi * np.imag(greens_function)
    data = matrix_element * spectral_function * fermi_dirac(x, 20.0)
    # BroadeningModel(lor_model, gau_model,)
    # data = convolve(gaussian_kernel(resolution=1e-3, x=x), data)
    data = add_noise(data, int(1e5))
    return xr.DataArray(data, coords=[x], dims=["eV"])
