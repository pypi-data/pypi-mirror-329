import xrfit

from peskit.fit.model import (
    BroadeningModel,
    FermiDiracModel,
    GaussianKernelModel,
    LorentzianModel,
)
from peskit.sim.cut import get_cut
from peskit.sim.edc import get_edc

__all__ = ["xrfit"]


def test_edc():
    edc = get_edc()
    model = (
        LorentzianModel(prefix="p0_") + LorentzianModel(prefix="p1_")
    ) * FermiDiracModel(prefix="f_")
    model = BroadeningModel(model, GaussianKernelModel())
    model.fit(x=edc.eV, data=edc, method="least_squares")


def test_user():
    cut = get_cut()
    model = LorentzianModel(prefix="p0_") * FermiDiracModel(prefix="f_")
    model = BroadeningModel(model, GaussianKernelModel(resolution=0.001))
    cut.fit(model=model, input_core_dims="eV")
