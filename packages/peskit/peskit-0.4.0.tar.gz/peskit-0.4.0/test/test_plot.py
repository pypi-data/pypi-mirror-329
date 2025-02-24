import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from peskit.plot.axis import set_axis
from peskit.plot.colorbar import set_colorbar
from peskit.plot.figure import get_figsize
from peskit.plot.label import set_label


def test_set_label():
    fig, axes = plt.subplots(2, 2)
    set_label(
        axes=axes,
        suffix="",
        fontsize="small",
        loc="upper center",
    )
    for ax in axes.flatten():
        anchored_texts = [
            a for a in ax.artists if isinstance(a, matplotlib.offsetbox.AnchoredText)
        ]
        assert anchored_texts, "Label not set on axes"


def test_get_figsize():
    width, height = get_figsize(
        col="single", width_scale=1.0, style="aps", height_scale=1.0
    )
    assert width > 0, "Invalid figure width"
    assert height > 0, "Invalid figure height"


def test_set_colorbar():
    fig, ax = plt.subplots()
    rng = np.random.default_rng()
    data = rng.random((10, 10))
    cax = ax.imshow(data)
    cbar = set_colorbar(
        ax=ax, mappable=cax, width=4.0, aspect=5.0, pad=3.0, orientation="vertical"
    )
    assert cbar is not None, "Colorbar not created"


def test_set_axis():
    fig, ax = plt.subplots()
    set_axis(ax.xaxis, scale=1e-3, num_ticks=3, label_pad=-9)
    assert ax.xaxis.get_major_formatter() is not None, "Axis formatter not set"
    assert ax.xaxis.get_major_locator() is not None, "Axis locator not set"
    assert ax.xaxis.labelpad == -9, "Axis label pad not set"
