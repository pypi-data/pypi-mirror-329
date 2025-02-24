import numpy as np
from lmfit import Model
from lmfit.models import COMMON_INIT_DOC

from peskit.fit.lorentzian.function import lorentzian


class LorentzianModel(Model):
    r"""A model based on a Lorentzian or Cauchy-Lorentz distribution function.

    The model has three Parameters: `amplitude`, `center`, and `sigma`. In
    addition, parameters `fwhm` and `height` are included as constraints
    to report full width at half maximum and maximum peak height,
    respectively.

    .. math::

        f(x; A, \mu, \sigma) = \frac{A}{\pi} \big[\frac{\sigma}{(x - \mu)^2 + \sigma^2}\big]

    where the parameter `amplitude` corresponds to :math:`A`, `center` to
    :math:`\mu`, and `sigma` to :math:`\sigma`. The full width at half
    maximum is :math:`2\sigma`.

    For more information, see:
    https://en.wikipedia.org/wiki/Cauchy_distribution

    """

    fwhm_factor = 2.0
    height_factor = 1.0 / np.pi

    def __init__(
        self,
        independent_vars=["x"],
        prefix="",
        nan_policy="raise",
        **kwargs,
    ):
        kwargs.update(
            {
                "prefix": prefix,
                "nan_policy": nan_policy,
                "independent_vars": independent_vars,
            }
        )
        super().__init__(lorentzian, **kwargs)
        self._set_paramhints_prefix()

    def _set_paramhints_prefix(self):
        self.set_param_hint("center", value=0.0, min=-np.inf, max=np.inf)
        self.set_param_hint("amplitude", value=1.0, min=0.0, max=np.inf)
        self.set_param_hint("sigma", value=1e-1, min=0, max=1.0)
        # self.set_param_hint("sigma", min=0)
        # self.set_param_hint("fwhm", expr=fwhm_expr(self))
        # self.set_param_hint("height", expr=height_expr(self))

    #     def post_fit(self, result):
    #         addpar = result.params.add
    #         prefix = self.prefix
    #         addpar(name=f'{prefix}fwhm', expr=fwhm_expr(self))
    #         addpar(name=f'{prefix}height', expr=height_expr(self))

    # def guess(self, data, x, negative=False, **kwargs):
    #     """Estimate initial model parameter values from data."""
    #     pars = guess_from_peak(self, data, x, negative, ampscale=1.25)
    #     return update_param_vals(pars, self.prefix, **kwargs)

    __init__.__doc__ = COMMON_INIT_DOC
    # guess.__doc__ = COMMON_GUESS_DOC


# class LorentzianModel(Model):
#     """A model based on a Lorentzian or Cauchy-Lorentz distribution function."""

#     def __init__(self, independent_vars=['x'], prefix='', nan_policy='raise',
#                  **kwargs,):
#         kwargs.update({'prefix': prefix, 'nan_policy': nan_policy,
#                        'independent_vars': independent_vars})
#         super().__init__(lorentzian, **kwargs)

#     def guess(self, data, x, negative=False, **kwargs):
#         """Estimate initial model parameter values from data."""
#         pars = self.make_params()
#         pars[f"{self.prefix}center_real"].set(value=x.mean(), min=x.min()*2, max=x.max()*2)
#         pars[f"{self.prefix}center_imag"].set(value=-0.1, max=0, min=-1.0)
#         pars[f"{self.prefix}amplitude_real"].set(value=1.0, min=1e-4, max=100.0)
#         return update_param_vals(pars, self.prefix, **kwargs)

#     __init__.__doc__ = COMMON_INIT_DOC
#     guess.__doc__ = COMMON_GUESS_DOC
