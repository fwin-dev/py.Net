from types import ClassType
from Lang.FuncTools.Abstraction import abstractmethod
from abc import ABCMeta

class MetaDescriptor(object):
	__metaclass__ = ABCMeta
	_allProtos = set()
	
	@classmethod
	def register(cls):
		cls._allProtos.add(cls)
	@classmethod
	def find(cls, protoWanted):
		"""Find protocol by class type or name of class."""
		candidates = []
		for proto in cls._allProtos:
			assert isinstance(protoWanted, str) or isinstance(protoWanted, ClassType)
			if (isinstance(protoWanted, str) and proto.getName().lower() == protoWanted.lower()) or proto == protoWanted:
				candidates.append(proto)
		assert len(candidates) <= 1
		if len(candidates) == 1:
			return candidates[0]
		else:
			return None
	
	@classmethod
	@abstractmethod
	def getName(cls):
		"""This is the name that can be passed to find() in order to find the class. Case insensitive."""
		pass
	@classmethod
	def getClass_Descriptor_Client(cls):
		return NotImplemented
	@classmethod
	def getClass_Descriptor_Server(cls):
		return NotImplemented
	@classmethod
	def getClass_Interface_Client(cls):
		"""
		Return the class/interface that defines any special methods needed for innerProtos to implement this protocol.
		
		Return None when no special methods to support this protocol are needed.
		"""
		return None
	@classmethod
	def getClass_Interface_Server(cls):
		"""
		Return the class/interface that defines any special methods needed for innerProtos to implement this protocol.
		
		Return None when no special methods to support this protocol are needed.
		"""
		return None

