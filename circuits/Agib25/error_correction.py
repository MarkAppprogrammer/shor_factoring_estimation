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
      # rembember CNOT is equivalent to the classical XOR 
      
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
   
   def add(self, n=None, runway=False):
      """Cost of full adder modulo 2 (with ancilla qubits)"""
      if n is None:
         n = self.params.n + self.params.deviation_padding
      if runway:
         """
         piece_count = int(math.ceil(params.n / params.runway_sep)) number of pieces
         piece_len = params.runway_sep + params.deviation_padding length of each piece
         """
         n = self.params.runway_sepration + self.params.deviation_padding
      return (n - 2) * (self.maj + self.uma) + 3*self.cnot + self.and_complete
   
   def new_adder(self, n=None, runway=False):
      """Cost of full new adder"""
      if n is None:
         n = self.params.n + self.params.deviation_padding
      if runway:
         n = self.params.runway_sepration + self.params.deviation_padding
      return (n - 3) * (self.and_complete) + self.toffoli + (n - 2)*self.cnot + self.gategen
   
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
      return self.and_uncomp + 2*self.cnot + self.gategen
   
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
               # + 2*floor(w/2)*self.gategen  # CZ same cost as CNOT
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
               + 0.5*m*(self.semi_clasical_comparison(n + m) + self.gategen))
   
   def modular_exp_windowed(self):
      n, ne, we, wm, m = self.params.n, self.params.n_e, self.params.windowed_exp, self.params.windowed_mult, self.params.deviation_padding

      nb = 2 * (ne/we) * (n + m)/wm
      classical_error = PhysicalCost(2**(-m), 0)
      return (nb*(self.new_adder(runway=False) + self.look_unlookup() + classical_error)
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
      if self.params.windowed:
         nb = (n + m)/wm
         res = nb*(self.new_adder() + self.look_unlookup())
         return res._replace(p=None)
      else:
         nb = n + m
         res = nb*self.semi_classical_ctrl_ctrl_add()
         return res._replace(p=None)

# need class to determine the cost of elementary gates
class ThreeDGaugeCode(CorrectionCode):
   """3d gauge color codes, with code switching."""

   def __init__(self, params: params):
      """Create 3d gauge color codes instance."""
      # Start and parameters validation
      super().__init__(params)
      d = params.extra_opts.distance  # pylint: disable=C0103
      debitage = params.extra_opts.debitage
      if not d % 2 == 1:
         raise ValueError("Distance must be odd.")
      if debitage not in (1, 2):
         raise ValueError("'debitage' takes value '1' or '2'.")

      # Geometrical characteristics
      self.memory_qubits = (d**3 + d)//2
      self.space_modes = ((1 + 3*d**2)//4 if debitage == 1
                           else (3*d**2 + 2*d - 3)//2)
      self.time_modes = 2*d-4 if debitage == 1 else d-2

      # Processor
      # 2 because 2 logical qubits, 2 because ancillary qubits for measurements
      self.proc_qubits = 2*2*self.space_modes

      # Logical gates
      # p_th = 0.0031  # arXiv:1503.08217
      p_th = 0.0075  # arXiv:1708.07131 ; known decoding
      # p_th = 0.019   # arXiv:1708.07131 ; no decoding
      A = 0.033
      α = 0.516
      β = 0.822
      # logical error: arXiv:1503.08217
      err = A * exp(α * log(params.gate_error_rate/p_th) * d**β)
      err_2 = 1 - (1 - err)**2
      # 2 factor: one time for gate, one time for stabilizers measurement
      # actual correction delayed to next use and neglected.
      time = 2*params.cycle_time*self.time_modes
      # T, T^\daggger, H, S, S^\dagger, CNOT and CZ transversal
      self.gategen = PhysicalCost(err, time)
      self.cnot = PhysicalCost(err_2, time)
      self.init = PhysicalCost(err, time/2)  # 1 pass
      self.measure = PhysicalCost(err, params.reaction_time + time/2)
      self.correct_time = time/2

   @property
   def and_uncomp(self):
      """AND uncomputation.

      Measurement-based technique is most of the time more efficient.
      """
      if self.params.measure_based_uncomp:
         return super().and_uncomp
      else:
         # Only gates before last CNOT in Fig.4 of arXiv:1805.03662
         return 5*self.gategen + 3*self.cnot
