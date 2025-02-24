import numpy as np
from lmfit import CompositeModel
from lmfit.models import LorentzianModel

from peskit.common.function import convolve
from peskit.fit.broadening.model import GaussianKernel


def test_convolve():
    x = np.linspace(-10, 5, 200)
    lor_model = LorentzianModel()
    gau_model = GaussianKernel()
    lor_b_model = CompositeModel(lor_model, gau_model, convolve)
    lor_b = lor_b_model.eval(x=x, center=-4, broadening=0.001)
    expected_values = np.array(
        [
            0.01015227,
            0.01032643,
            0.01051497,
            0.01071859,
            0.01093799,
            0.01117391,
            0.01142709,
            0.01169833,
            0.01198842,
            0.01229824,
            0.01262871,
            0.01298079,
            0.01335554,
            0.01375409,
        ]
    )

    assert np.allclose(lor_b[:14], expected_values), (
        f"Expected {expected_values}, but got {lor_b[:14]}"
    )
