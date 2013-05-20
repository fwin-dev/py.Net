from Net.Protocols import base

import lxml.etree
import re

"""
Implementation of the HELD ID protocol in python.

Follows RFC 6155, but not all identification types are implemented yet:
http://tools.ietf.org/html/rfc6155
@author: Jesse Cowles
"""

class HELD_ID(base.DescriptorXML):
	def __init__(self):
		super(HELD_ID, self).__init__()
	@classmethod
	def getClass_Descriptor_Server(cls):
		return HELD_ID_Descriptor_Server
	@classmethod
	def getClass_Descriptor_Client(cls):
		return None
HELD_ID.register()

class HELD_ID_Descriptor_Server(HELD_ID, base.Descriptor_Server):
	"""responseTime attribute described in the RFC is ignored."""
	_namespace = {"heldID": "urn:ietf:params:xml:ns:geopriv:held:id"}
	def __init__(self):
		super(HELD_ID_Descriptor_Server, self).__init__()
	def pickle(self, cucumbers, *args, **kwargs):
		raise NotImplementedError()
	
	def _unpickle_XML_getOptions(self):
		return {"parser": lxml.etree.XMLParser(ns_clean=True), "base_url": None}
	
	def unpickle_XML(self, xmlEtree, clientInfo, *args, **kwargs):
		# Parse device URI if it exists (optional)
		deviceURInode = xmlEtree.xpath("/heldID:device/heldID:uri", namespaces=self._namespace)
		if len(deviceURInode) == 1:
			keyTmp = deviceURInode[0].text
		elif len(deviceURInode) == 0:
			deviceURInode = xmlEtree.xpath("//*[local-name() = 'uri']")
			if (len(deviceURInode) == 1):
				keyTmp = deviceURInode[0].text
			elif len(deviceURInode) == 0:
				raise BadIdentifier(tooMany=True)
		else:
			raise BadIdentifier(isMissing=True)
		# URI item found, let's see its content
		if re.match(self.heldKeyRegex, keyTmp) is not None:
			key = re.match(self.heldKeyRegex, keyTmp).group()
		else:
			raise BadIdentifier(isWrongFormat=True)
		
		deviceObjs = 
		return {"cucumbers": (deviceObj,), "innerProtoBody": None}

class HELD_ID_Request(base.Cucumber.Request):
	pass

class HELD_ID_Device(HELD_ID_Request):
	def __init__(self, idType, idValue):
		self.type = idType
		"""Type of ID value. Must be one of: 'IP', TODO"""
		self.value = idValue
		"""ID value of the client making the request. Could be the client's IP, phone number, etc."""

class XML_IP(HELD_ID_Request):
	def __init__(self, IP, version):
		self.IP = IP
		self.version = version
class XML_MAC(HELD_ID_Request):
	def __init__(self, MAC):
		self.MAC = MAC
class XML_IP_Port(HELD_ID_Request):
	def __init__(self, IP, version, port, protocol):
		"""
		version		--- 4 or 6
		protocol	--- TCP, UDP, etc.
		"""
		self.IP = IP
		self.version = version
		self.port = port
		self.protocol = protocol

class HELD_ID_Error(base.Cucumber.Response, Exception):
	"""Corresponds to RFC 5985 error response when the location request cannot be fulfilled."""
	def __init__(self, nameInRFC, message=None):
		Exception.__init__(self, message)
		self.name = self.__class__.__name__
		self.code = nameInRFC
	def __str__(self):
		return "HELD_ID " + self.name + (": " + self.message if self.message != None else "")

class BadIdentifier(HELD_ID_Error):
	"""
	Indicates that a Device identifier used in the HELD request is not supported, badly formatted,
	or not one for which the client was authorized.
	
	Only one argument must be true.
	"""
	def __init__(self, msg, isMissing=False, tooMany=False, isWrongFormat=False, isNotAuthorized=False):
		assert len(filter(lambda x: x == True, (isMissing, tooMany, isWrongFormat, isNotAuthorized))) == 1
		if isMissing:			msg = "Device identifier is missing"
		elif tooMany:			msg = "Only 1 device identifier is allowed"
		elif isWrongFormat:		msg = "Device identifier is badly formatted"
		elif isNotAuthorized:	msg = "Client is not authorized for this identifier"
		HELD_ID_Error.__init__(self, "badIdentifier", "Bad identifier: " + msg)

