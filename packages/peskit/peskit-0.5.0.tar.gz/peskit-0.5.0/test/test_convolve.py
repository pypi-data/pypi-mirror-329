import numpy as np

from peskit.fit.model import BroadeningModel, GaussianKernelModel, LorentzianModel


def test_convolve():
    x = np.linspace(-10, 5, 200)
    lor_model = LorentzianModel()
    gau_model = GaussianKernelModel()
    lor_b_model = BroadeningModel(
        lor_model,
        gau_model,
    )
    lor_b = lor_b_model.eval(x=x, center=-4, broadening=0.001)
    expected_values = np.array(
        [
            0.00583577,
            0.00626735,
            0.00671181,
            0.00716842,
            0.00763649,
            0.00811543,
            0.00860478,
            0.00910419,
            0.00961349,
            0.0101327,
            0.01066201,
            0.01120186,
            0.0117529,
            0.012316,
        ]
    )

    assert np.allclose(lor_b[:14], expected_values), (
        f"Expected {expected_values}, but got {lor_b[:14]}"
    )
