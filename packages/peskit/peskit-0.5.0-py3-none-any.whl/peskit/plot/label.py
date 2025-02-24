from typing import Literal

import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def set_label(
    axes=None,
    values: np.ndarray | None = None,
    startfrom: int = 1,
    order: Literal["C", "F", "A", "K"] = "C",
    loc: Literal[
        "upper left",
        "upper center",
        "upper right",
        "center left",
        "center",
        "center right",
        "lower left",
        "lower center",
        "lower right",
    ] = "upper left",
    offset: tuple[float, float] = (0, 0),  # (7,0)
    prefix: str = "(",
    suffix: str = ")",
    numeric: bool = False,
    capital: bool = False,
    fontweight: Literal[
        "ultralight",
        "light",
        "normal",
        "regular",
        "book",
        "medium",
        "roman",
        "semibold",
        "demibold",
        "demi",
        "bold",
        "heavy",
        "extra bold",
        "black",
    ] = "normal",
    fontsize: (
        float
        | Literal[
            "xx-small", "x-small", "small", "medium", "large", "x-large", "xx-large"
        ]
        | None
    ) = None,
    **kwargs,
):
    r"""Labels subplots with automatically generated labels.

    Parameters
    ----------
    axes
        `matplotlib.axes.Axes` to label. If an array is given, the order will be
        determined by the flattening method given by `order`.
    values
        Integer or string labels corresponding to each Axes in `axes` for
        manual labels.
    startfrom
        Start from this number when creating automatic labels. Has no
        effect when `values` is not `None`.
    order
        Order in which to flatten `ax`. 'C' means to flatten in
        row-major (C-style) order. 'F' means to flatten in column-major
        (Fortran- style) order. 'A' means to flatten in column-major
        order if a is Fortran contiguous in memory, row-major order
        otherwise. 'K' means to flatten a in the order the elements
        occur in memory. The default is 'C'.
    loc
        The box location. The default is ``'upper left'``.
    offset
        Values that are used to position the legend in conjunction with
        `loc`, given in display units.
    prefix
        String to prepend to the alphabet label.
    suffix
        String to append to the alphabet label.
    numeric
        Use integer labels instead of alphabets.
    capital
        Capitalize automatically generated alphabetical labels.
    fontweight
        Set the font weight. The default is ``'normal'``.
    fontsize
        Set the font size. The default is ``'medium'`` for axes, and ``'large'`` for
        figures.
    **kwargs
        Extra arguments to `matplotlib.text.Text`: refer to the `matplotlib`
        documentation for a list of all possible arguments.
    """
    r"""Labels subplots with automatically generated labels.
    Parameters
    ----------
    axes
        `matplotlib.axes.Axes` to label. If an array is given, the order will be
        determined by the flattening method given by `order`.
    values
        Integer or string labels corresponding to each Axes in `axes` for
        manual labels.
    startfrom
        Start from this number when creating automatic labels. Has no
        effect when `values` is not `None`.
    order
        Order in which to flatten `ax`. 'C' means to flatten in
        row-major (C-style) order. 'F' means to flatten in column-major
        (Fortran- style) order. 'A' means to flatten in column-major
        order if a is Fortran contiguous in memory, row-major order
        otherwise. 'K' means to flatten a in the order the elements
        occur in memory. The default is 'C'.
    loc
        The box location. The default is ``'upper left'``.
    offset
        Values that are used to position the legend in conjunction with
        `loc`, given in display units.
    prefix
        String to prepend to the alphabet label.
    suffix
        String to append to the alphabet label.
    numeric
        Use integer labels instead of alphabets.
    capital
        Capitalize automatically generated alphabetical labels.
    fontweight
        Set the font weight. The default is ``'normal'``.
    fontsize
        Set the font size. The default is ``'medium'`` for axes, and ``'large'`` for
        figures.
    **kwargs
        Extra arguments to `matplotlib.text.Text`: refer to the `matplotlib`
        documentation for a list of all possible arguments.
    """

    kwargs["fontweight"] = fontweight
    if plt.rcParams["text.usetex"] & (fontweight == "bold"):
        prefix = "\\textbf{" + prefix
        suffix = suffix + "}"
        kwargs.pop("fontweight")

    axlist = np.array(axes, dtype=object).flatten(order=order)

    # Remove unwanted axes from the list using get_label
    axlist = [ax for ax in axlist if ax.get_label() not in ("<colorbar>", "dummy")]
    if values is None:
        values = np.array([i + startfrom for i in range(len(axlist))], dtype=np.int64)
    else:
        values = np.array(values).flatten(order=order)
        if not (len(axlist) == len(values)):
            raise IndexError(
                "The number of given values must match the number of given axes."
            )

    for i in range(len(axlist)):
        bbox_to_anchor = axlist[i].bbox
        if fontsize is None:
            if isinstance(axlist[i], matplotlib.figure.Figure):
                fs = "large"
            else:
                fs = "medium"
        else:
            fs = str(fontsize)

        bbox_transform = matplotlib.transforms.ScaledTranslation(
            offset[0] / 72, offset[1] / 72, axlist[i].get_figure().dpi_scale_trans
        )
        label_str = _alph_label(values[i], prefix, suffix, numeric, capital)
        # with plt.rc_context({"text.color": axes_textcolor(axlist[i])}):
        #     at = matplotlib.offsetbox.AnchoredText(
        #         label_str,
        #         loc=loc,
        #         frameon=False,
        #         pad=0,
        #         borderpad=0.5,
        #         prop=dict(fontsize=fs, **kwargs),
        #         bbox_to_anchor=bbox_to_anchor,
        #         bbox_transform=bbox_transform,
        #         clip_on=False,
        #     )
        at = matplotlib.offsetbox.AnchoredText(
            label_str,
            loc=loc,
            frameon=False,
            pad=0,
            borderpad=0.5,
            prop=dict(fontsize=fs, **kwargs),
            bbox_to_anchor=bbox_to_anchor,
            bbox_transform=bbox_transform,
            clip_on=False,
        )
        axlist[i].add_artist(at)


def _alph_label(val, prefix, suffix, numeric, capital):
    # Generate labels from string or integer.
    if isinstance(val, (int | np.integer)) or val.isdigit():
        if numeric:
            val = str(val)
        else:
            ref_char = "A" if capital else "a"
            val = chr(int(val) + ord(ref_char) - 1)
    elif not isinstance(val, str):
        raise TypeError("Input values must be integers or strings.")
    return prefix + val + suffix
