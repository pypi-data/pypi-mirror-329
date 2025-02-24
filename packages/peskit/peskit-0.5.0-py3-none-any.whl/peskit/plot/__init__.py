import os

import matplotlib as mpl

from peskit.plot.axis import set_axis
from peskit.plot.colorbar import set_colorbar
from peskit.plot.figure import get_figsize
from peskit.plot.label import set_label

__all__ = [
    "get_figsize",
    "set_axis",
    "set_colorbar",
    "set_label",
]
mpl.style.core.USER_LIBRARY_PATHS.append(
    os.path.join(os.path.dirname(__file__), "stylelib")
)

mpl.style.core.reload_library()
mpl.style.core.reload_library()
