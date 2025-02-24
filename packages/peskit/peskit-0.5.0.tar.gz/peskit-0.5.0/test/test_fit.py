import numpy as np
import pytest
import xarray as xr
from lmfit import Parameters

# from lmfit import ModelResult, Parameters
from lmfit.model import ModelResult

from peskit.fit.fermi_dirac.model import FermiDiracLinbkgBroadModel
from peskit.fit.fermi_dirac.wrapper import calibrate_fd, fit_fd


@pytest.fixture
def data_array():
    coords_x = np.linspace(-0.1, 0.1, 100)
    coords_y = np.linspace(-0.1, 0.1, 100)
    data = np.exp(-(coords_x[:, None] ** 2) / 0.01) * np.exp(
        -(coords_y[None, :] ** 2) / 0.01
    )
    return xr.DataArray(data, coords=[coords_x, coords_y], dims=["eV", "y"])


@pytest.fixture
def model_result():
    params = Parameters()
    params.add("center", value=0.0)
    params.add("temp", value=300.0)
    params.add("resolution", value=0.01)
    return ModelResult(FermiDiracLinbkgBroadModel(), params, None)


def test_calibrate_fd(data_array, model_result):
    calibrated_da = calibrate_fd(data_array, model_result)
    assert "fermi_level_shift" in calibrated_da.attrs
    assert "temp" in calibrated_da.attrs
    assert "resolution_mdc" in calibrated_da.attrs
    assert np.isclose(calibrated_da.attrs["fermi_level_shift"], 0.0)
    assert np.isclose(calibrated_da.attrs["temp"], 300.0)
    assert np.isclose(calibrated_da.attrs["resolution_mdc"], 0.01)


def test_fit_fd(data_array):
    result = fit_fd(data_array, "eV")
    assert isinstance(result, ModelResult)
    assert "center" in result.params
    assert "temp" in result.params
    assert "resolution" in result.params
