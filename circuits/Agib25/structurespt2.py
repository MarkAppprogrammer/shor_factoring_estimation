from collections import namedtuple
import datetime

# structures needed for gs21

# algorithm options
algorithm_options = namedtuple(
                              'algorithm_options',
                              'n, ne, we, m, windowed, measure_based',
                              defaults=(None, None, None, None, None, True, True))

# low level options
lowlevel_options = namedtuple('lowlevel_options', 'debitage, d1, d, tc, tr, pp',
                              defaults=(2, None, None, 1e-6, 1e-6, 1e-3))

# combination of all
paramaters = namedtuple('Params', 'type, algo, low_level')

class PhysicalCost(namedtuple('PhysicalCost', ('p', 't'))):
   """
      Class helps calcuate the cost of elementary gates using the error probability and runtime

   """

   def __add__(self, other):
      if not isinstance(other, __class__):
         return NotImplemented
      return __class__(1 - (1 - self.p)*(1 - other.p), self.t + other.t)

# structures needed for ge21

# parameters for algorithm
Parameters = namedtuple(
    'Parameters',
    [
        # Physical gate error rate.
        ('gate_err', float),
        # Time it takes to trigger a logical measurement, error correct it,
        # and decide which measurement to do next.
        ('reaction_time', datetime.timedelta),
        # Time it takes to measure the surface code's local stabilizers.
        ('cycle_time', datetime.timedelta),
        # Window size over exponent bits. (g0 in paper)
        ('exp_window', int),
        # Window size over multiplication bits. (g1 in paper)
        ('mul_window', int),
        # Bits between runways used during parallel additions. (g2 in paper)
        ('runway_sep', int),
        # Level 2 code distance.
        ('code_distance', int),
        # Level 1 code distance.
        ('l1_distance', int),
        # Error budget.
        ('max_total_err', float),
        # Problem size.
        ('n', int),
        # Number of controlled group operations required.
        ('n_e', int),
        # Whether or not to use two levels of 15-to-1 distillation.
        ('use_t_t_distillation', bool), # 5 distillation not required
        # Number of bits of padding to use for runways and modular coset.
        ('deviation_padding', int),
    ]
)

# derivation proptries 
DeviationProperties = namedtuple(
    'DeviationProperties',
    [
        ('piece_count', int),
        ('piece_len', int),
        ('reg_len', int),
        ('inner_loop_count', int),
        ('deviation_error', float),
    ]
)

# cost estimate
CostEstimate = namedtuple(
    'CostEstimate',
    [
        ('params', Parameters),
        ('toffoli_count', int),
        ('total_error', float),
        ('distillation_error', float),
        ('topological_data_error', float),
        ('total_hours', float),
        ('total_megaqubits', int),
        ('total_volume_megaqubitdays', float)
    ]
)