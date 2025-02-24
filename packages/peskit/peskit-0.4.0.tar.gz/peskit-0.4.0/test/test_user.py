from lmfit import CompositeModel

from peskit.common.function import convolve
from peskit.fit.broadening.model import GaussianKernel
from peskit.fit.fermi_dirac.model import FermiDiracModel
from peskit.fit.lorentzian.model import LorentzianModel
from peskit.sim.edc import get_edc


def test_user():
    edc = get_edc()
    model = LorentzianModel(prefix="p_") * FermiDiracModel(prefix="f_")
    model = CompositeModel(model, GaussianKernel(), convolve)
    model.fit(x=edc.eV, data=edc, method="least_squares")
