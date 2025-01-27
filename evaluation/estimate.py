"""
Cost Estimate

Last Updated: 1/26/2025
@author: Mark Agib
"""

from math import ceil, isnan, isinf, log
import matplotlib.pyplot as plt
import datetime
import csv
from itertools import product

from structures import *
from error_correction import *

"""
def estimate_best(n, num_mod_mult, gate_error):
   print(n)
   print(num_mod_mult)
   print(gate_error)
"""
def fips_strength_level(n):
    # From FIPS 140-2 IG CMVP, page 110.
    #
    # This is extrapolated from the asymptotic complexity of the sieving
    # step in the general number field sieve (GNFS).
    ln = log
    return (1.923 * (n * ln(2))**(1/3) * ln(n * ln(2))**(2/3) - 4.69) / ln(2)

def fips_strength_level_rounded(n): # NIST-style rounding
    return 8 * round(fips_strength_level(n) / 8)


# RSA removed  -> Optional[CostEstimate] from all below
def eh_rsa(n): # Single run.
    
    delta = 20 # Required to respect assumptions in the analysis.
    m = ceil(n / 2) - 1
    l = m - delta
    n_e = m + 2 * l
    return n_e #estimate_best(n, n_e)


# def eh_rsa_max_tradeoffs(n): # With maximum tradeoffs.
#     return estimate_best(n, math.ceil(n / 2))


# General DLP
def shor_dlp_general(n):
    delta = 5 # Required to reach 99% success probability.
    m = n - 1 + delta
    n_e = 2 * m
    return n_e


def eh_dlp_general(n): # Single run.
    m = n - 1
    n_e = 3 * m
    return n_e


# def eh_dlp_general_max_tradeoffs(n): # Multiple runs with maximal tradeoff.
#     m = n - 1
#     n_e = m
#     return estimate_best(n, n_e)


# Schnorr DLP
def shor_dlp_schnorr(n):
    delta = 5 # Required to reach 99% success probability.
    z = fips_strength_level_rounded(n)
    m = 2 * z + delta
    n_e = 2 * m
    return n_e


def eh_dlp_schnorr(n): # Single run.
    z = fips_strength_level_rounded(n)
    m = 2 * z
    n_e = 3 * m
    return n_e


# def eh_dlp_schnorr_max_tradeoffs(n): # Multiple runs with maximal tradeoff.
#     z = fips_strength_level_rounded(n)
#     m = 2 * z
#     n_e = m
#     return estimate_best(n, n_e)


# Short DLP
def eh_dlp_short(n):
    z = fips_strength_level_rounded(n)
    m = 2 * z
    n_e = 3 * m
    return n_e


def eh_dlp_short_max_tradeoffs(n): # Multiple runs with maximal tradeoff.
    z = fips_strength_level_rounded(n)
    m = 2 * z
    n_e = m
    return n_e


#______Ancillary Functions______

#verb? + NEEDS CHECKING
def memory_limited_time(err_corr: CorrectionCode):
   """Cycle-time when limited by memory readout time."""
   # Time to access 1 qubit with 4Γ/10 hypothesis
   speed = 4 * 12e6 / 10  # qubit/s
   return qubits_in_mem(err_corr) / speed

def correct_all(err_corr: CorrectionCode):
   """Compute time for error-correcting all the memory."""
   return err_corr.correct_time*logical_qubit_count(err_corr.params,)/2

def modes_in_mem(err_corr: CorrectionCode):
   return(err_corr.space_modes*logical_qubit_count(err_corr.params), err_corr.time_modes)

def qubits_in_mem(err_corr: CorrectionCode):
   return err_corr.memory_qubits*logical_qubit_count(err_corr.params)

def logical_qubit_count(params: params): ## figure out wear from + 
   if params.windowed:
      count = 4 * params.n + 3 * params.deviation_padding + params.windowed_exp - 1
   else: 
      count = 3*(params.n + params.deviation_padding) + 1
   return count

#_______________________________

def iterate(params: params, **kwargs):
   """kwargs can be passed ex: wes and wms"""
   if type(params.extra_opts) is gsOptions: ## need to add itarete for gate error and moduli + check if this works
      ranges = dict(d1s=(None,),
                    ds=range(1, 100, 2),
                    wes=range(1, 10),
                    wms=range(1, 10),
                    ms=range(1, 40)) ## change padding? for runways
      #print(ranges)
   else: ## add for None?
      raise ValueError("params.extra_opts not valid!")
   ranges.update(kwargs)
   for d1, d, we, wm, m in product(ranges['d1s'], ranges['ds'], ranges['wes'],
                                   ranges['wms'], ranges['ms']):
      if wm is not None and we is not None and wm > we:
         continue
      yield params._replace(  ##cleared
         windowed_exp=we,
         windowed_mult=wm,
         deviation_padding=m,
         extra_opts=params.extra_opts._replace(fs_distance=d1, distance=d)
      )
      
def rank(cost: PhysicalCost, qubits, bias=1):
   return cost.exp_t * qubits**bias  ## update cost.exp_t

def prepare_resources(params: params):
   err_corr = CorrectionCode(params) ## needs updating
   cost = err_corr.modular_exp()
   qubits = err_corr.proc_qubits
   return cost, qubits

def find_best(beg_params: params, bias=1):  ## cleared
   best = float('inf') ## infiniti
   best_params = None

   for params in iterate(beg_params):
      try:
         cost, qubits = prepare_resources(params)
      except RuntimeError:
         continue
      score = rank(cost, qubits, bias)
      if score < best: ## update score
         best = score
         best_params = params
   if best_params == None: ## wasn't updated
      print("An optmization didn't converge (ran out of time)")
   return best_params

##_________________________________________________


def unit_format(num, unit, unicode=False):
   """Assemble number and unit, eventually converting it into LaTeX."""
   space = chr(8239)
   num = str(round(num)) if not isinf(num) else "∞" if unicode else r"\infty"
   if not unicode:
      unit = {"µs": r"\micro\second",
               "ms": r"\milli\second",
               "s": r"\second",
               "min": r"\minute",
               "hours": "hours",
               "days": "days"}[unit]
   if unicode:
      return num + space + unit
   return rf"\SI{{{num}}}{{{unit}}}"


def format_time(time, unicode=False):
   """Return formatted time, with correct unity."""
   if isnan(time):
      return "nan"
   if time < 1e-3:
      temps, unit = time*1e6, "µs"
   elif time < 1:
      temps, unit = time*1000, "ms"
   elif time < 60:
      temps, unit = time, "s"
   elif time < 3600:
      temps, unit = time/60, "min"
   elif time < 3600*24:
      temps, unit = time/3600, "hours"
   else:
      temps, unit = time/(3600*24), "days"
   return unit_format(temps, unit, unicode)


"""
gate_error_rates = [1e-3, 1e-4]
num_bits = [1024, 2048, 3072, 4096, 8192, 12288, 16384]


for num_bit in num_bits:
   for gate_error in gate_error_rates:
      shor(num_bit, gate_error)
"""

if __name__ == '__main__':

   #start

   #typing.NamedTuple doesn't offer defaults :(
   gate_error_rates = [1e-3, 1e-4]
   num_bits = [1024, 2048, 3072, 4096, 8192, 12288, 16384]

   datasets = [
      ("RSA, via Ekera-HÃ¥stad with s = 1 in a single run:", eh_rsa),
      ("Discrete logarithms, Schnorr group, via Shor:", shor_dlp_schnorr),
      ("Discrete logarithms, Schnorr group, via Ekera-HÃ¥stad with s = 1 in a single run:", eh_dlp_schnorr),
      ("Discrete logarithms, short exponent, via EkerÃ¥-HÃ¥stad with s = 1 in a single run:", eh_dlp_short),
      ("Discrete logarithms, general, via Shor:", shor_dlp_general),
      ("Discrete logarithms, general, via EkerÃ¥ with s = 1 in a single run:", eh_dlp_general),
   ]

   for name, func in datasets:
      for n in num_bits:
         test_params = params(n=n, n_e=func(n), windowed_exp=None, windowed_mult=None,
                        cycle_time=1e-6, reaction_time=1e-6, measure_based_uncomp=True,
                        windowed=True, deviation_padding=None, gate_error_rate=1e-3,
                        extra_opts=gsOptions(2, None, None)
         )

         best_params = find_best(test_params)
         best_err_corr = CorrectionCode(best_params)
         cost, qubits = prepare_resources(best_params)
         total_hours = cost.exp_t / 60 ** 2
         total_megaqubits = qubits / 10 ** 6
         total_volume_megaqubitdays = (total_hours / 24) * total_megaqubits

         with open('estimates.csv', 'a', encoding="utf8") as file:
            file.write(
            f"{best_params}, {cost}, {qubits}, "
            f"{str(best_err_corr.temps_inter_lectures())}, "
            f"{qubits_in_mem(best_err_corr)}, "
            f"{format_time(correct_all(best_err_corr), True)}, "
            f"{format_time(cost.exp_t * memory_limited_time(best_err_corr) / best_params.cycle_time, unicode=True)}, "
            f"{total_hours}, {total_megaqubits}, {total_volume_megaqubitdays}\n"
            )

         del test_params
