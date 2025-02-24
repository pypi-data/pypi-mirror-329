"""Module for Loading Igor Binary Wave (.ibw) files."""

import os

import igor2
import igor2.record
import numpy as np
import xarray as xr


def load_ibw(
    wave: dict | igor2.record.WaveRecord | str | os.PathLike,
    data_dir: str | os.PathLike | None = None,
) -> xr.DataArray:
    """Load a wave from Igor binary format.

    Parameters
    ----------
    wave
        The wave to load. It can be provided as a dictionary, an instance of
        `igor2.record.WaveRecord`, or a string representing the path to the wave file.
    data_dir
        The directory where the wave file is located. This parameter is only used if
        `wave` is a string or `PathLike` object. If `None`, `wave` must be a valid path.

    Returns
    -------
    xarray.DataArray
        The loaded wave.

    Raises
    ------
    ValueError
        If the wave file cannot be found or loaded.
    TypeError
        If the wave argument is of an unsupported type.

    """
    DEFAULT_DIMS = ["W", "X", "Y", "Z"]
    _MAXDIM = 4

    if isinstance(wave, dict):
        wave_dict = wave
    elif isinstance(wave, igor2.record.WaveRecord):
        wave_dict = wave.wave
    else:
        if data_dir is not None:
            wave = os.path.join(data_dir, wave)
        wave_dict = igor2.binarywave.load(wave)

    d = wave_dict["wave"]
    version = wave_dict["version"]
    dim_labels = [""] * _MAXDIM
    bin_header, wave_header = d["bin_header"], d["wave_header"]
    if version <= 3:
        shape = [wave_header["npnts"]] + [0] * (_MAXDIM - 1)
        sfA = [wave_header["hsA"]] + [0] * (_MAXDIM - 1)
        sfB = [wave_header["hsB"]] + [0] * (_MAXDIM - 1)
        # data_units = wave_header["dataUnits"]
        axis_units = [wave_header["xUnits"]]
        axis_units.extend([""] * (_MAXDIM - len(axis_units)))
    else:
        shape = wave_header["nDim"]
        sfA = wave_header["sfA"]
        sfB = wave_header["sfB"]
        if version >= 5:
            # data_units = d["data_units"].decode()
            axis_units = [b"".join(d).decode() for d in wave_header["dimUnits"]]
            units_sizes = bin_header["dimEUnitsSize"]
            sz_cum = 0
            for i, sz in enumerate(units_sizes):
                if sz != 0:
                    axis_units[i] = d["dimension_units"][sz_cum : sz_cum + sz].decode()
                sz_cum += sz
            for i, sz in enumerate(bin_header["dimLabelsSize"]):
                if sz != 0:
                    dim_labels[i] = b"".join(d["labels"][i]).decode()
        else:
            # data_units = d["data_units"].decode()
            axis_units = [d["dimension_units"].decode()]

    coords = {}
    for i, (a, b, c) in enumerate(zip(sfA, sfB, shape, strict=True)):
        if c == 0:
            continue

        dim, unit = dim_labels[i], axis_units[i]

        if dim == "":
            if unit == "":
                dim = DEFAULT_DIMS[i]
            else:
                # If dim is empty, but the unit is not, use the unit as the dim name
                dim, unit = unit, ""

        coords[dim] = np.linspace(b, b + a * (c - 1), c)
        if unit != "":
            coords[dim] = xr.DataArray(coords[dim], dims=(dim,), attrs={"units": unit})

    attrs: dict[str, int | float | str] = {}
    for ln in d.get("note", b"").decode().splitlines():
        if "=" in ln:
            key, value = ln.split("=", maxsplit=1)
            try:
                attrs[key] = int(value)
            except ValueError:
                try:
                    attrs[key] = float(value)
                except ValueError:
                    attrs[key] = value

    return xr.DataArray(
        d["wData"], dims=coords.keys(), coords=coords, attrs=attrs
    ).rename(wave_header["bname"].decode())
