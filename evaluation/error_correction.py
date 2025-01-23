from math import exp, log, floor, ceil

from structures import Params

class CorrectionCode:

   def __init__(self, params: Params):
      self.params = params

      # elmentary gates cost
      self.gategen = None # hadmards, s, t, and z gates
      self.cnot = None 
      self.init = None # intilazation of a new qubits
      self.measure = None # measurement of ONE qubit

   
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
