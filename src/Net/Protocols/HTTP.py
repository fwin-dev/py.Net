import protocol

import urllib2
from abc import abstractmethod

class HTTP(protocol.Descriptor):
	"""
	Follows HTTP 1.1 specification (RFC 2616).
	
	http://www.w3.org/Protocols/rfc2616/rfc2616.html
	"""
	@classmethod
	def getClass_Descriptor_Client(cls):
		return NotImplemented
	@classmethod
	def getClass_Descriptor_Server(cls):
		return HTTP_Descriptor_Response
	@classmethod
	def getClass_Interface_Client(cls):
		return None
	@classmethod
	def getClass_Interface_Server(cls):
		return HTTP_Interface_Server
	
	def pickle_validateCucumbers(self, cucumbers, *args, **kwargs):
		"""Returns False when protocol is invalid. Returns cucumbers when everything is ok."""
		if not hasattr(cucumbers, "__iter__"):
			cucumbers = (cucumbers,)
		
		for innerProto in cucumbers:
			if not isinstance(innerProto, HTTP_Interface_Server):
				return False
		
		# there can only be 1 error class
		if len(filter(isinstance(innerProto, HTTP_Interface_Server), cucumbers)) > 1:
			return False
		
		return cucumbers

HTTP.register()


class HTTP_Descriptor_Response(protocol.Descriptor_Server, HTTP):
	def pickle_validateCucumbers(self, cucumbers, *args, **kwargs):
		cucumbers = super(HTTP_Descriptor_Response, self).pickle_validateCucumbers(cucumbers, *args, **kwargs)
		if cucumbers == False:
			cucumbers = HTTP_Error(500, "Internal Server Error")
		return cucumbers
	
	def pickle(self, cucumbers, serverInfo, *args, **kwargs):
		
		
	def unpickle(self, fileObj, clientInfo, parentCucumbers, *args, **kwargs):
		


class HTTP_Interface_Server(protocol.Cucumber_Interface_Server, HTTP):
	def getHTTPprotocolVersion(self):
		return "HTTP/1.1"
	@abstractmethod
	def getContentType(self):
		pass
	@abstractmethod
	def getResponseCode(self):
		pass

class HTTP_Error(protocol.Cucumber_Response, HTTP_Interface_Server, urllib2.HTTPError):
	def __init__(self, code, reason):
		HTTP_Interface_Server.__init__(self)
		urllib2.HTTPError.__init__(self, url=None, code=code, msg=reason, hdrs=None, fp=None)
	def getResponseCode(self):
		return str(self.code) + " " + self.reason
	def getContentType(self):
		return None
