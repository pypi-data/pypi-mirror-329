import numpy as np
import xarray as xr
from scipy.ndimage import gaussian_filter1d

from peskit.common.distribution import fermi_dirac
from peskit.common.function import add_noise


def get_cut() -> xr.DataArray:
    x = np.linspace(-0.1, 0.01, 200)
    y = np.linspace(-0.1, 0.1, 200)
    self_energy = 0.05 * x - 1j * 0.05 * x**2 - 1j * 0.01

    bare_band = -1.0 * y
    matrix_element = 2.0 + y * 0.0
    greens_function = 1 / (
        x[:, np.newaxis] - bare_band[np.newaxis, :] - self_energy[:, np.newaxis]
    )
    spectral_function = -1 / np.pi * np.imag(greens_function)
    data = matrix_element * spectral_function * fermi_dirac(x, 20.0)
    data = gaussian_filter1d(data, sigma=1.0)
    data = add_noise(data, int(1e6))
    return xr.DataArray(data.T, coords=[x, y], dims=["eV", "kx"])
