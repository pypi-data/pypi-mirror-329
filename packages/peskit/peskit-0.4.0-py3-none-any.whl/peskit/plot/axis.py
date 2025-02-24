import matplotlib.ticker as ticker
from matplotlib.axis import Axis
from matplotlib.ticker import MaxNLocator


def set_axis(
    axis: Axis,
    scale: float | None = 1e-3,
    num_ticks: int | None = 3,
    label_pad: int | None = -9,
    # tick_params: dict | None = None,
):
    """
    Set the properties of a matplotlib axis.

    Parameters
    ----------
    axis : matplotlib.axis.Axis
        The axis to configure.
    scale : float, optional
        The scale factor for the axis labels. Default is 1e-3.
    num_ticks : int, optional
        The number of ticks on the axis. Default is 3.
    label_pad : int, optional
        The padding between the axis and its label. Default is 30.

    """
    if scale is not None:
        formatter = ticker.FuncFormatter(lambda x, pos: f"{x / scale:g}")
        axis.set_major_formatter(formatter)
    if num_ticks is not None:
        axis.set_major_locator(MaxNLocator(nbins=num_ticks))
    if label_pad is not None:
        axis.labelpad = label_pad
    # if tick_params is not None:
    #     axis.set_tick_params(**tick_params)
