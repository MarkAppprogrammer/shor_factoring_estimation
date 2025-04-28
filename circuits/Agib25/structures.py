"""
Structures for cost estimate

Last Updated: 1/26/2025
@author: Mark Agib
"""

from collections import namedtuple
from typing import NamedTuple, Union
import datetime
import numbers

gsOptions = NamedTuple(
   'Parameters',
   [
      ('debitage', int),
      ('fs_distance', int),
      ('distance', int)
   ]
)
gsOptions.__doc__ = """

Élie Gouzien and Nicolas Sangouard (3D color gauge codes + memory) specfic optmization parameters

Parameters:
   debitage:      cut of tetrahedron for '3dcolor' error correction code
                     1 is parallel to large tetrahedron face
                     2 is as presented in article (orthogonal to two faces)
   fs_distance:   distance of first step of distillation
   distance:      main code distance
"""

geOptions = NamedTuple(
   'Parameters',
   [
      ('l2_distance', int),
      ('l1_distance', int),
      ('err_budget', float),
      ('t_distillation', bool)
   ]
)
geOptions.__doc__ = """

Craig Gidney and Martin Ekera specfic optmization parameters

Parameters:
   l2_distance:      level 2 surface code distance
   l1_distance:      level 1 surface code distance
   err_budget:       maximun total error budget
   t_distillation:   wheter or not to use two levels of distillation
"""

params = NamedTuple(
   'Parameters', 
   [
      ('n', int),
      ('n_e', int),
      ('windowed_exp', int),
      ('windowed_mult', int),
      ('cycle_time', datetime.timedelta),
      ('reaction_time', datetime.timedelta),
      ('measure_based_uncomp', bool),
      ('windowed', bool),
      ('runway_sepration', int),
      ('deviation_padding', int),
      ('gate_error_rate', float),
      ('extra_opts', Union[geOptions, gsOptions])
   ]
)
params.__doc__ = """

Parameters:
   n:                      number of bits of N
   n_e:                    number of bits of the exponent
   windowed_exp:           window size over exponent bits
   windowed_mult:          window size over multiplicaiton bits
   cycle_time:             time taken to measure the surface code's stablizers
   reaction_time:          time it takes to detect and correct error
   measure_based_uncomp:   whether or not meaurement based uncompuation of the AND gates should  be used
   windowed:               whether or not windowing should be used
   runway_sepration:       number of bits needed between runways
   deviation_padding:      padding nesscary due to approxmation of coset represntation as well as runways
   gate_error_rate:        error rate assumed for each gate e.g. 1e-3 or 1e-4
"""

#_______________________________________________________Work in Progress_______________________________________________________


class PhysicalCost(namedtuple('PhysicalCost', ('p', 't'))):
    """Physical cost of some gates: error probability and runtime.

    Attributs
    ---------
        p : error probability.
        t : runtime.

    Methods
    -------
        Has same interface as namedtuple, except for listed operators.

    Operators
    ---------
        a + b : cost of serial execution of a and b.
        k * a : cost of serial execution of a k times (k can be float).
        a | b : cost of parallel execution of a and b.

    """

    def __add__(self, other):
        """Cost of sequential execution of self and other."""
        if not isinstance(other, __class__):
            return NotImplemented
        return __class__(1 - (1 - self.p)*(1 - other.p), self.t + other.t)

    def __mul__(self, other):
        """
        Cost of sequential execution of self other times.

        Other does not need to be integer (as some gates are probabilistically
                                           applied).
        """
        if not isinstance(other, numbers.Real):
            return NotImplemented
        return __class__(1 - (1 - self.p)**other, self.t * other)

    def __rmul__(self, other):
        """Right multiplication."""
        return self * other

    def __sub__(self, other):
        """Subtraction: revert previous of future addition."""
        return self + (-1 * other)

    def __or__(self, other):
        """Cost of parallel execution of self and other."""
        if not isinstance(other, __class__):
            return NotImplemented
        return __class__(1 - (1 - self.p)*(1-other.p), max(self.t, other.t))

    @property
    def exp_t(self):
        """Average runtime (several intents might be required)."""
        if self.p is None:
            return self.t
        if self.p >= 1:
            return float('inf')
        return self.t / (1 - self.p)

    @property
    def exp_t_str(self):
        """Format average runtime."""
        try:
            return datetime.timedelta(seconds=self.exp_t)
        except OverflowError:
            if self.exp_t == float('inf'):
                return "∞"
            return str(round(self.exp_t/(3600*24*365.25))) + " years"

    def __str__(self):
        """Readable representation of a PhysicalCost."""
        # pylint: disable=C0103
        try:
            t = datetime.timedelta(seconds=self.t)
        except OverflowError:
            if self.t == float('inf'):
                t = "∞"
            else:
                t = str(round(self.t/(3600*24*365.25))) + " years"
        return f"PhysicalCost(p={self.p}, t={t}, exp_t={self.exp_t_str})"