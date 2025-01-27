from math import exp, log, floor, ceil

from structures import *

class CorrectionCode:
   def __new__(cls, params: params, *args, **kwargs):
      if cls is CorrectionCode:
         if type(params.extra_opts) is gsOptions:
            return ThreeDGaugeCode(params, *args, **kwargs)
         else:
            raise ValueError("Not a valid set of extra options")
      return super().__new__(cls)

   def __init__(self, params: params):
      self.params = params

      # elmentary gates cost
      self.gategen = None # hadmards, s, t, and z gates
      self.cnot = None 
      self.init = None # intilazation of a new qubits
      self.measure = None # measurement of ONE qubit

      # processor
      self.correct_time = None  # time for correcting one logical qubit
      self.proc_qubits = None # physical qubits = to 1 logical qubit

      # mem
      self.memory_qubits = None
      self.space_modes = None
      self.time_modes = None

   
   @property
   def and_g(self):
      """Cost of AND computation"""
      # |T> intlization is also assumed to be a T gate
      return self.init + self.gategen*6 + self.cnot*3
   
   @property
   def and_uncomp(self):
      # hadmard gate comined with state prep
      return self.measure + 0.5*self.cnot
   
   @property 
   def and_complete(self):
      return self.and_g + self.and_uncomp
   
   @property
   def toffoli(self):
      try:
         return self._toffoli
      except AttributeError:
         return self.and_complete + self.cnot 
      # because a toffoli is literatly |a,b,c> -> |a,b,c XOR (a AND b)>
      
   @toffoli.setter
   def toffoli(self, value):
      self._toffoli = value
   
   @toffoli.deleter
   def toffoli(self):
      del self._toffoli

   @property
   def maj(self):
      return self.and_g + 3*self.cnot
   
   @property
   def uma(self):
      return 3*self.cnot + self.and_uncomp
   
   def add(self, n=None):
      """Cost of full adder modulo 2 (with ancill qubits)"""
      return (n - 2) * (self.maj + self.uma) + 3*self.cnot + self.and_complete
   
   def new_adder(self, n=None):
      """Cost of full new adder"""
      return (n - 3) * (self.and_complete) + self.toffoli + 2*self.cnot + self.gategen
   
   @property
   def semi_classical_ctrl_maj(self):
        return self.and_g + 3*self.cnot
   
   @property
   def semi_classical_ctrl_uma(self):
      return self.and_uncomp + 2.5*self.cnot
   
   def semi_classical_ctrl_add(self, n=None):
      if n is None:
         n = self.params.n + self.params.deviation_padding
      return ((n - 2)*(self.semi_classical_ctrl_maj
                        + self.semi_classical_ctrl_uma)
               + 2*self.cnot + 0.5*self.and_uncomp)
   
   def semi_classical_ctrl_ctrl_add(self, n=None):
      return self.and_uncomp + self.semi_classical_ctrl_add(n)
   
   @property
   def semi_classical_maj(self): #no ctrl
      return self.and_g + 2*self.cnot + self.gategen
   
   @property
   def semi_classical_maj_dag(self):
      return self.and_uncomp + 2*self.cnot + self.gate1
   
   def semi_clasical_comparison(self, n=None):
      if n is None:
         n = self.params.n + self.params.deviation_padding
      return ((n - 1)*(self.semi_classical_maj
                     + self.semi_classical_maj_dag)
               + self.cnot)
   
   #need windowed part
   def lookup_sizes(self):
      w = self.params.windowed_exp + self.params.windowed_mult #total window size
      return w, self.params.n
   
   def lookup(self, w=None, n=None):
      if w is None and n is None:
         w, n = self.lookup_sizes()
      return (2*self.gategen + (2**w - 2 + 2**w * n/2) * self.cnot
               + (2**w - 2) * self.and_complete)

   def unary_ununairy(self, size=None):
      # first NOT is not counted as |1> can be directly initialized.
      if size is None:
         size = floor((self.params.windowed_exp + self.params.windowed_exp)/2)
      return self.init + 2*(size - 1)*self.cnot + (size - 1)*self.and_complete

   def unlookup(self, w=None, n=None):
      # Hadamard gates are merged with preparation/measurement.
      if w is None and n is None:
         w, n = self.lookup_sizes()
      return (n*self.measure
               + self.unary_ununairy(floor(w/2))
               # + 2*floor(w/2)*self.gate1  # CZ same cost as CNOT
               + self.lookup(w=ceil(w/2), n=floor(w/2)))

   def look_unlookup(self, w=None, n=None):
      if w is None and n is None:
         w, n = self.lookup_sizes()
      return self.lookup(w, n) + self.unlookup(w, n)
   
   def initialize_coset_reg(self):
      # Hadamard gates are merged with preparation/measurement.
      n, m = self.params.n, self.params.deviation_padding
      return (m*(self.init + self.measure)
               + m*self.semi_classical_ctrl_add(n + m)
               + 0.5*m*(self.semi_classical_comparison(n + m) + self.gategen))
   
   def modular_exp_windowed(self):
      n, ne, we, wm, m, _, _ = self.params.n, self.params.n_e, self.params.windowed_exp,
      self.params.windowed_mult, self.params.deviation_padding

      nb = 2 * (ne/we) * (n + m)/wm
      classical_error = PhysicalCost(2**(-m), 0)
      return (nb*(self.add() + self.look_unlookup() + classical_error)
               + 2*self.initialize_coset_reg())
   
   def modular_exp_controlled(self):
      n, ne, m= self.params.n, self.params.n_e, self.params.deviation_padding
      nb = 2 * ne * (n + m)
      classical_error = PhysicalCost(2**(-m), 0)
      return (nb*(self.semi_classical_ctrl_ctrl_add() + classical_error)
               + 2 * self.initialize_coset_reg()
               + ne*(n + m)*(2*self.cnot + self.toffoli))

   def modular_exp(self):
      if self.params.windowed:
         return self.modular_exp_windowed()
      return self.modular_exp_controlled()
   
   def temps_inter_lectures(self):
      # Time of one product-addition
      n, wm, m= self.params.n, self.params.windowed_mult, self.params.deviation_padding
      if self.params.algo.windowed:
         nb = (n + m)/wm
         res = nb*(self.add() + self.look_unlookup())
         return res._replace(p=None)
      else:
         nb = n + m
         res = nb*self.semi_classical_ctrl_ctrl_add()
         return res._replace(p=None)

# need class to determine the cost of elementary gates
class ThreeDGaugeCode(CorrectionCode):
   print("test")
