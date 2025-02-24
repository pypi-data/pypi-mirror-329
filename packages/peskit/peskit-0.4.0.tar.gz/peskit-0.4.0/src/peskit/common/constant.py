import numpy as np

# Boltzmann constant : in units of eV / Kelvin
CONST_KB: float = 8.617333262145178e-5
# Kinentic Energy constant : in units eV * angstrom**2
CONST_KE: float = 3.8099821161548606
# From :mod:`lmfit.lineshapes`, equal to `numpy.finfo(numpy.float64).resolution`
TINY: float = 1.0e-15
# Sqrt of 2 * pi
S2PI: float = np.sqrt(2 * np.pi)
