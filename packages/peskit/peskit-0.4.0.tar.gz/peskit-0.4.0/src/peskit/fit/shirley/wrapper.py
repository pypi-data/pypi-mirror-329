import warnings

import numpy as np
import xarray as xr

__all__ = ["remove_shirley"]


def remove_shirley(
    darray: xr.DataArray,
    xrange: tuple = (0.02, None),
    xdim: str = "eV",
):
    darray_above_EF = darray.sel({xdim: slice(*xrange)})
    background_above_EF = darray_above_EF.mean(dim=xdim)

    darray_without_const_background = darray - background_above_EF
    shirley_background = get_shirley_background_full_range(
        darray_without_const_background
    )

    result_darray = darray_without_const_background - shirley_background
    result_darray.attrs = darray.attrs
    return result_darray


def _get_shirley_background_full_range(
    xps: np.ndarray,
    eps=1e-7,
    max_iters=50,
    n_samples=5,
) -> np.ndarray:
    background = np.copy(xps)
    cumulative_xps = np.cumsum(xps, axis=0)
    total_xps = np.sum(xps, axis=0)

    rel_error = np.inf

    i_left = np.mean(xps[:n_samples], axis=0)
    i_right = np.mean(xps[-n_samples:], axis=0)

    iter_count = 0

    k = i_left - i_right
    for _ in range(max_iters):
        cumulative_background = np.cumsum(background, axis=0)
        total_background = np.sum(background, axis=0)

        new_bkg = np.copy(background)

        for i in range(len(new_bkg)):
            new_bkg[i] = i_right + k * (
                (
                    total_xps
                    - cumulative_xps[i]
                    - (total_background - cumulative_background[i])
                )
                / (total_xps - total_background + 1e-5)
            )

        rel_error = np.abs(np.sum(new_bkg, axis=0) - total_background) / (
            total_background
        )

        background = new_bkg

        if np.any(rel_error < eps):
            break

    if (iter_count + 1) == max_iters:
        warnings.warn(
            "Shirley background calculation did not converge "
            + f"after {max_iters} steps with relative error {rel_error}!",
            stacklevel=2,
        )

    return background


def get_shirley_background_full_range(
    xps: xr.DataArray,
    eps=1e-7,
    max_iters=50,
    n_samples=5,
) -> xr.DataArray:
    # xps = normalize_to_spectrum(xps).copy(deep=True)

    core_dims = [d for d in xps.dims if d != "eV"]

    return xr.apply_ufunc(
        _get_shirley_background_full_range,
        xps,
        eps,
        max_iters,
        n_samples,
        input_core_dims=[core_dims, [], [], []],
        output_core_dims=[core_dims],
        exclude_dims=set(core_dims),
        vectorize=False,
    )


# def get_shirley_background(
#     xps: xr.DataArray,
#     energy_range: slice | None = None,
#     eps=1e-7,
#     max_iters=50,
#     n_samples=5,
# ) -> xr.DataArray:
#     if energy_range is None:
#         energy_range = slice(None, None)

#     xps_for_calc = xps.sel(eV=energy_range)

#     bkg = get_shirley_background_full_range(
#         xps_for_calc, eps, max_iters, n_samples
#     )
#     bkg = bkg.transpose(*xps.dims)
#     full_bkg = xps * 0

#     left_idx = np.searchsorted(full_bkg.eV.values, bkg.eV.values[0], side="left")
#     right_idx = left_idx + len(bkg)

#     full_bkg.values[:left_idx] = bkg.values[0]
#     full_bkg.values[left_idx:right_idx] = bkg.values
#     full_bkg.values[right_idx:] = bkg.values[-1]

#     return full_bkg
