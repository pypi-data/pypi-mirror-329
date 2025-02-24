import xarray as xr

from peskit.io.loader import load_ibw


def test_load_ibw():
    # Define a sample wave dictionary
    wave_dict = {
        "wave": {
            "bin_header": {
                "dimEUnitsSize": [0, 0, 0, 0],
                "dimLabelsSize": [0, 0, 0, 0],
            },
            "wave_header": {
                "npnts": 10,
                "hsA": 1.0,
                "hsB": 0.0,
                "xUnits": b"",
                "nDim": [10, 0, 0, 0],
                "sfA": [1.0, 0.0, 0.0, 0.0],
                "sfB": [0.0, 0.0, 0.0, 0.0],
                "dimUnits": [b"", b"", b"", b""],
                "bname": b"test_wave",
            },
            "wData": list(range(10)),
            "note": b"key1=1\nkey2=2.0\nkey3=value",
        },
        "version": 5,
    }

    # Load the wave using the load_ibw function
    data_array = load_ibw(wave_dict)
    # Check the type of the returned object
    assert isinstance(data_array, xr.DataArray)

    # Check the name of the DataArray
    assert data_array.name == "test_wave"

    # Check the data values
    assert (data_array.values == list(range(10))).all()

    # Check the attributes
    assert data_array.attrs["key1"] == 1
    assert data_array.attrs["key2"] == 2.0
    assert data_array.attrs["key3"] == "value"

    # Check the coordinates
    assert "W" in data_array.coords
    assert (data_array.coords["W"].values == list(range(10))).all()
