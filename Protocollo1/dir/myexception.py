# -*- coding: iso-8859-15 -*-
######################################################
#	classe dell'eccezione che viene sollevata quando si riceve un pacchetto
#	che non si riesce a riconoscere
#

######################################################

class PackTypeNotDefinedException(Exception):
	
	def __init__ (self, value):
		self.value = value
		
	def __str__ (self):
		 return repr(self.value)
		
class PackLengthNotValid(Exception):
	
	def __init__ (self, value):
		self.value = value
		
	def __str__ (self):
		return repr(self.value)
	
class SessionIdNotExist(Exception):
	
	def __init__ (self, value):
		self.value = value
	
	def __str__(self):
		return repr(self.value)