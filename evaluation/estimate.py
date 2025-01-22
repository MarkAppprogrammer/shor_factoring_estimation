import math
import matplotlib.pyplot as plt
import datetime

from structures import *


def estimate_best(n, num_mod_mult, gate_error):
   print(n)
   print(num_mod_mult)
   print(gate_error)

def estimate():
   return None


def shor(n, gate_error):
  # based on ekera post processing estimation
   padding = 20
   m = math.ceil(n / 2) - 1
   l = m - padding
   num_mod_mult = m + 2 * l
   return estimate_best(n, num_mod_mult, gate_error)

gate_error_rates = [1e-3, 1e-4]
num_bits = [1024, 2048, 3072, 4096, 8192, 12288, 16384]

for num_bit in num_bits:
   for gate_error in gate_error_rates:
      shor(num_bit, gate_error)

