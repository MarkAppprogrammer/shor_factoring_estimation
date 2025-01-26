"""
Structures for cost estimate

Last Updated: 1/26/2025
@author: Mark Agib
"""

#from collections import namedtuple
from typing import NamedTuple, Union
import datetime

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
      #('runway_sepration', int),
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
