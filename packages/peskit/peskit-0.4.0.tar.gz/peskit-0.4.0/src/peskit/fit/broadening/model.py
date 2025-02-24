import lmfit as lf

from peskit.fit.broadening.function import gaussian_kernel


class GaussianKernel(lf.Model):
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
