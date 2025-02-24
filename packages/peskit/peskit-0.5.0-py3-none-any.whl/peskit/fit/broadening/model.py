import lmfit as lf
import numpy as np
from lmfit import CompositeModel

from peskit.fit.broadening.function import gaussian_kernel


def convolve(model, resolution):
    r"""Convolution of resolution with model data.

    It is assumed that the resolution FWHM is energy independent.
    We multiply by spacing :math:`dx` of independent variable :math:`x`.

    .. math:: (model \otimes resolution)[n] = dx * \sum_m model[m] * resolution[m-n]

    Parameters
    ----------
    model : numpy.ndarray
        model data
    resolution : numpy.ndarray
        resolution data

    Returns
    -------
    numpy.ndarray
    """
    c = np.convolve(model, resolution, mode="valid")
    if len(model) % len(resolution) == 0:
        c = c[:-1]
    return c


class BroadeningModel(CompositeModel):
    r"""Convolution between model and resolution.

    It is assumed that the resolution FWHM is energy independent.
    Non-symmetric energy ranges are allowed (when the range of negative values
    is different than that of positive values).

    The convolution requires multiplication by the X-spacing to preserve
    normalization
    """

    def __init__(self, resolution, model, **kws):
        super().__init__(resolution, model, convolve, **kws)
        self.resolution = resolution
        self.model = model

    def eval(self, params=None, **kwargs):
        res_data = self.resolution.eval(params=params, **kwargs)
        # evaluate model on an extended energy range to avoid boundary effects
        independent_var = self.resolution.independent_vars[0]
        e = kwargs[independent_var]  # energy values
        neg_e = min(e) - np.flip(e[np.where(e > 0)], axis=0)
        pos_e = max(e) - np.flip(e[np.where(e < 0)], axis=0)
        e = np.concatenate((neg_e, e, pos_e))
        kwargs.update({independent_var: e})
        model_data = self.model.eval(params=params, **kwargs)
        # Multiply by the X-spacing to preserve normalization
        de = (e[-1] - e[0]) / (len(e) - 1)  # energy spacing
        return de * convolve(model_data, res_data)


class GaussianKernelModel(lf.Model):
    """Model for Gaussian convolution."""

    def __init__(
        self,
        independent_vars=["x"],
        prefix="",
        missing="drop",
        name=None,
        resolution: float | None = None,
        **kwargs,
    ):
        """Defer to lmfit for initialization."""
        kwargs.update(
            {"prefix": prefix, "missing": missing, "independent_vars": independent_vars}
        )
        self.resolution = resolution
        super().__init__(gaussian_kernel, **kwargs)
        self._set_paramhints_prefix()

    def _set_paramhints_prefix(self):
        self.set_param_hint("resolution", value=0.01, min=1e-5, max=2e-2)

    def guess(self, data, x=None, **kwargs):
        pars = self.make_params()
        # pars[f"{self.prefix}center"].set(value=0.0, vary=False)
        if self.resolution is not None:
            pars[f"{self.prefix}resolution"].set(value=self.resolution, vary=False)
        else:
            pars[f"{self.prefix}resolution"].set(value=0.01, min=1e-5, max=2e-2)
        # pars[f"{self.prefix}amplitude"].set(value=1.0, vary=False)
        return lf.models.update_param_vals(pars, self.prefix, **kwargs)

    __init__.__doc__ = lf.models.COMMON_INIT_DOC
    guess.__doc__ = lf.models.COMMON_GUESS_DOC
