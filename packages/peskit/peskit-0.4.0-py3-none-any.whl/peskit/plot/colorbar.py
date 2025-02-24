from collections.abc import Iterable, Sequence
from numbers import Number
from typing import Any, Literal, cast

import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def set_colorbar(
    ax: matplotlib.axes.Axes | Iterable[matplotlib.axes.Axes] | None = None,
    mappable: matplotlib.cm.ScalarMappable | None = None,
    width: float = 4.0,
    aspect: float = 5.0,
    pad: float = 3.0,
    minmax: bool = False,
    plusminus: bool = False,
    orientation: Literal["vertical", "horizontal"] = "vertical",
    floating=False,
    ticklabels: Sequence[str] | None = None,
    **kwargs,
):
    r"""Create a colorbar with fixed width and aspect to ensure uniformity of plots.

    Parameters
    ----------
    ax
        The `matplotlib.axes.Axes` instance in which the colorbar is drawn.
    mappable
        The mappable whose colormap and norm will be used.
    width
        The width of the colorbar in points.
    aspect
        aspect ratio of the colorbar.
    pad
        The pad between the colorbar and axes in points.
    minmax
        If `False`, the ticks and the ticklabels will be determined from the keyword
        arguments (the default). If `True`, the minimum and maximum of the colorbar will
        be labeled.
    orientation
        Colorbar orientation.
    **kwargs
        Keyword arguments are passed to `proportional_colorbar`.

    Returns
    -------
    cbar : matplotlib.colorbar.Colorbar
        The created colorbar.

    """
    is_horizontal = orientation == "horizontal"

    if ax is None:
        ax = plt.gca()

    if floating:
        if isinstance(ax, np.ndarray):
            if ax.ndim == 1:
                parent = ax[-1]
            elif ax.ndim == 2:
                parent = ax[0, -1]
            else:
                raise ValueError
        else:
            parent = ax

        cbar = _proportional_colorbar(
            mappable=mappable,
            ax=ax,
            cax=_gen_cax(parent, width, aspect, pad, is_horizontal),
            orientation=orientation,
            **kwargs,
        )

    else:
        if isinstance(ax, Iterable):
            if not isinstance(ax, np.ndarray):
                ax = np.array(ax, dtype=object)
            bbox = matplotlib.transforms.Bbox.union(
                [
                    x.get_position(original=True)
                    .frozen()
                    .transformed(x.figure.transFigure)
                    .transformed(x.figure.dpi_scale_trans.inverted())
                    for x in ax.flat
                ]
            )
        else:
            fig = ax.get_figure()

            if fig is None:
                raise RuntimeError("Axes is not attached to a figure")

            bbox = (
                ax.get_position(original=True)
                .frozen()
                .transformed(fig.transFigure)
                .transformed(fig.dpi_scale_trans.inverted())
            )

        if orientation == "horizontal":
            kwargs["anchor"] = (1, 1)
            kwargs["location"] = "top"
            kwargs["fraction"] = width / (72 * bbox.height)
            kwargs["pad"] = pad / (72 * bbox.height)
            kwargs["shrink"] = width * aspect / (72 * bbox.width)
        else:
            kwargs["anchor"] = (0, 1)
            kwargs["fraction"] = width / (72 * bbox.width)
            kwargs["pad"] = pad / (72 * bbox.width)
            kwargs["shrink"] = width * aspect / (72 * bbox.height)

        cbar = _proportional_colorbar(
            mappable=mappable,
            ax=ax,
            aspect=aspect,
            panchor=(0, 1),
            orientation=orientation,
            **kwargs,
        )

    if minmax:
        if is_horizontal:
            cbar.set_ticks(cbar.ax.get_xlim())
        else:
            cbar.set_ticks(cbar.ax.get_ylim())
        cbar.set_ticklabels(("Min", "Max"))
        cbar.ax.tick_params(labelsize="small")

    if plusminus:
        if is_horizontal:
            cbar.set_ticks(cbar.ax.get_xlim())
        else:
            cbar.set_ticks(cbar.ax.get_ylim())
        cbar.set_ticklabels((r"$-$", r"$+$"))
        cbar.ax.tick_params(labelsize="small")

    if ticklabels is not None:
        cbar.set_ticklabels(ticklabels)

    if is_horizontal:
        cbar.ax.set_box_aspect(1 / aspect)
    else:
        cbar.ax.set_box_aspect(aspect)

    return cbar


def _gen_cax(ax, width=4.0, aspect=7.0, pad=3.0, horiz=False, **kwargs):
    w, h = width / 72, aspect * width / 72
    if horiz:
        cax = _ez_inset(ax, h, w, pad=(0, -w - pad / 72), **kwargs)
    else:
        cax = _ez_inset(ax, w, h, pad=(-w - pad / 72, 0), **kwargs)
    return cax


def _ez_inset(
    parent_axes: matplotlib.axes.Axes,
    width: float | str,
    height: float | str,
    pad: float | tuple[float, float] = 0.1,
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
    ] = "upper right",
    **kwargs,
) -> matplotlib.axes.Axes:
    fig = parent_axes.get_figure()
    if fig is None:
        raise RuntimeError("Parent axes is not attached to a figure")
    locator = InsetAxesLocator(parent_axes, width, height, pad, loc)
    ax_ = fig.add_axes(locator(parent_axes, None).bounds, **kwargs)
    ax_.set_axes_locator(locator)
    return ax_


class InsetAxesLocator:
    def __init__(self, ax, width, height, pad, loc):
        self._ax = ax
        self._transAxes = ax.transAxes
        self._width = width
        self._height = height
        self._loc = loc
        self.set_pad(pad)

    def __call__(self, ax, renderer):
        return matplotlib.transforms.TransformedBbox(
            matplotlib.transforms.Bbox.from_bounds(*self._size_to_bounds(ax)),
            self._transAxes
            + matplotlib.transforms.ScaledTranslation(
                self.pads[0], self.pads[1], ax.figure.dpi_scale_trans
            )
            - ax.figure.transSubfigure,
        )

    def set_pad(self, pad):
        pad_num = False
        if isinstance(pad, Number):
            pad_num = True
            pad = [pad, pad]
        self.pads = [-pad[0], -pad[1]]
        if "center" in self._loc:
            self.pads[0] *= -1
            self.pads[1] *= -1
            if "upper" in self._loc or "lower" in self._loc:
                if pad_num:
                    self.pads[0] = 0
                self.pads[1] *= -1
            elif "left" in self._loc or "right" in self._loc:
                if pad_num:
                    self.pads[1] = 0
                self.pads[0] *= -1
        if "left" in self._loc:
            self.pads[0] *= -1
        if "lower" in self._loc:
            self.pads[1] *= -1

    def add_pad(self, delta):
        self.pads[0] += delta[0]
        self.pads[1] += delta[1]

    def sizes(self, ax):
        ax_sizes = (
            ax.get_window_extent()
            .transformed(ax.figure.dpi_scale_trans.inverted())
            .bounds[2:]
        )
        return [
            float(sz[:-1]) / 100 if isinstance(sz, str) else sz / ax_sizes[i]
            for i, sz in enumerate([self._width, self._height])
        ]

    def _size_to_bounds(self, ax):
        sizes = self.sizes(ax)
        origin = [1 - sizes[0], 1 - sizes[1]]
        if "center" in self._loc:
            origin[0] /= 2
            origin[1] /= 2
            if "upper" in self._loc or "lower" in self._loc:
                origin[1] *= 2
            elif "left" in self._loc or "right" in self._loc:
                origin[0] *= 2
        if "left" in self._loc:
            origin[0] = 0
        if "lower" in self._loc:
            origin[1] = 0
        return origin + sizes


def _proportional_colorbar(
    mappable: matplotlib.cm.ScalarMappable | None = None,
    cax: matplotlib.axes.Axes | None = None,
    ax: matplotlib.axes.Axes | Iterable[matplotlib.axes.Axes] | None = None,
    **kwargs,
) -> matplotlib.colorbar.Colorbar:
    """
    Replace the current colorbar or creates a new colorbar with proportional spacing.

    The default behavior of colorbars in `matplotlib` does not support colors
    proportional to data in different norms. This function circumvents this behavior.

    Parameters
    ----------
    mappable
        The `matplotlib.cm.ScalarMappable` described by this colorbar.
    cax
        Axes into which the colorbar will be drawn.
    ax
        One or more parent axes from which space for a new colorbar axes
        will be stolen, if `cax` is `None`.  This has no effect if `cax`
        is set. If `mappable` is `None` and `ax` is given with more than
        one Axes, the function will try to infer the mappable from the
        first one.
    **kwargs
        Extra arguments to `matplotlib.pyplot.colorbar`: refer to the `matplotlib`
        documentation for a list of all possible arguments.

    Returns
    -------
    cbar : matplotlib.colorbar.Colorbar
        The created colorbar.

    Examples
    --------
    ::

        import numpy as np
        import matplotlib.pyplot as plt
        import matplotlib.colors

        # Create example data and plot
        X, Y = np.mgrid[0 : 3 : complex(0, 100), 0 : 2 : complex(0, 100)]
        pcm = plt.pcolormesh(
            X,
            Y,
            (1 + np.sin(Y * 10.0)) * X**2,
            norm=matplotlib.colors.PowerNorm(gamma=0.5),
            cmap="Blues_r",
            shading="auto",
        )

        # Plot evenly spaced colorbar
        proportional_colorbar()

    """
    fontsize = kwargs.pop("fontsize", None)

    if ax is None:
        if cax is None:
            ax = plt.gca()
            if mappable is None:
                mappable = _get_mappable(ax)
    elif isinstance(ax, Iterable):
        if not isinstance(ax, np.ndarray):
            ax = np.array(ax, dtype=object)
        i = 0
        while mappable is None and i < len(ax.flat):
            mappable = _get_mappable(ax.flatten()[i], silent=(i != (len(ax.flat) - 1)))
            i += 1
    elif mappable is None:
        mappable = _get_mappable(ax)

    if mappable is None:
        raise RuntimeError("No mappable was found to use for colorbar creation")

    if mappable.colorbar is None:
        plt.colorbar(mappable=mappable, cax=cax, ax=ax, **kwargs)
        mappable.colorbar = cast(matplotlib.colorbar.Colorbar, mappable.colorbar)

    ticks = mappable.colorbar.get_ticks()
    if cax is None:
        mappable.colorbar.remove()
    kwargs.setdefault("ticks", ticks)
    kwargs.setdefault("cmap", mappable.cmap)
    kwargs.setdefault("norm", mappable.norm)

    cbar = plt.colorbar(
        mappable=mappable,
        cax=cax,
        ax=ax,
        spacing="proportional",
        boundaries=kwargs["norm"].inverse(np.linspace(0, 1, kwargs["cmap"].N)),
        **kwargs,
    )
    if fontsize is not None:
        cbar.ax.tick_params(labelsize=fontsize)
    return cbar


def _get_mappable(
    ax: matplotlib.axes.Axes, image_only: bool = False, silent: bool = False
) -> matplotlib.cm.ScalarMappable | None:
    """Get the `matplotlib.cm.ScalarMappable` from a given `matplotlib.axes.Axes`.

    Parameters
    ----------
    ax
        Parent axes.
    image_only
        Only consider images as a valid mappable, by default `False`.
    silent
        If `False`, raises a `RuntimeError` when no mappable is found. If `True`,
        silently returns `None`.

    Returns
    -------
    matplotlib.cm.ScalarMappable or None

    """
    if not image_only:
        try:
            mappable: Any = ax.collections[-1]
        except (IndexError, AttributeError):
            mappable = None

    if image_only or mappable is None:
        try:
            mappable = ax.get_images()[-1]
        except (IndexError, AttributeError):
            mappable = None

    if mappable is None and not silent:
        raise RuntimeError(
            "No mappable was found to use for colorbar "
            "creation. First define a mappable such as "
            "an image (with imshow) or a contour set ("
            "with contourf)."
        )
    return mappable
