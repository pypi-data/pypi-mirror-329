import lmfit as lf
import xarray as xr

from peskit.fit.fermi_dirac.model import FermiDiracLinbkgBroadModel


def calibrate_fd(
    da: xr.DataArray,
    model_result: lf.model.ModelResult,
    coords: str = "eV",
) -> xr.DataArray:
    """Calibrate the DataArray by Fermi Dirac Model."""
    new_da = da.copy(deep=True)
    center = model_result.params["center"].value
    new_da = new_da.assign_coords({coords: new_da[coords] - center})
    new_da.attrs["fermi_level_shift"] = center
    new_da.attrs["temp"] = model_result.params["temp"].value
    new_da.attrs["resolution_mdc"] = model_result.params["resolution"].value
    return new_da


def fit_fd(
    da: xr.DataArray,
    coord: str,
    coord_range: tuple = (-0.02, 0.02),
    temp: float | None = None,
    resolution: float | None = None,
    **kws,
):
    assert coord in da.dims, f"Dimension '{coord}' not found in DataArray"
    if da.ndim != 2:
        raise NotImplementedError("DataArray should be 2D.")

    # Get MDC area
    sum_dims = [dim for dim in da.dims if dim != coord]
    mdc_area = da.sel({coord: slice(*coord_range)}).sum(dim=sum_dims).values
    x = da[coord].sel({coord: slice(*coord_range)}).values

    # Fit the MDC area with Fermi Dirac Model
    model = FermiDiracLinbkgBroadModel()
    params = model.guess(mdc_area, x=x)
    if temp is not None:
        params["temp"].set(value=temp, vary=False)
    if resolution is not None:
        params["resolution"].set(value=resolution, vary=False)
    return model.fit(mdc_area, x=x, params=params, **kws)
