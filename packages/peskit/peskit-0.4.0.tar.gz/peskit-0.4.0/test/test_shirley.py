import numpy as np
import xarray as xr

from peskit.fit.shirley.wrapper import remove_shirley


def test_remove_shirley():
    # Create a sample DataArray
    rng = np.random.default_rng()
    data = rng.random(100)
    coords = {"eV": np.linspace(-1, 1, 100)}
    darray = xr.DataArray(data, coords=coords, dims="eV")

    # Define x_range and x_dim
    xrange = (-1, 0.02)
    xdim = "eV"

    # Call the remove_shirley function
    result = remove_shirley(darray, xrange=xrange, xdim=xdim)

    # Check if the result is a DataArray
    assert isinstance(result, xr.DataArray)

    # Check if the result has the same coordinates and dimensions as the input
    xr.testing.assert_equal(result.coords, darray.coords)
    assert result.dims == darray.dims

    # Check if the result has the same attributes as the input
    assert result.attrs == darray.attrs
