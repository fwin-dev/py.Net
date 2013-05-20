from Net.Protocols import base
from HELD import HELD_Descriptor_Server

class _HELD(base.MetaDescriptor):
	def __init__(self):
		super(_HELD, self).__init__()
	def getName(self):
		return "HELD"
	@classmethod
	def getClass_Descriptor_Server(cls):
		return HELD_Descriptor_Server
_HELD.register()
