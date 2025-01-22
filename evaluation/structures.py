from collections import namedtuple
import datetime

#algorithm options
algorithm_options = namedtuple(
                              'algorithm_options',
                              'n, ne, we, m, windowed, measure_based, Simplification',
                              defaults=(None, None, None, None, None, True, True, False))
