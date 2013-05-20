import Cucumbers
import lxml.etree

class HELD_Error(Cucumbers.HELD_Cucumber, Exception):
	"""Corresponds to an RFC 5985 general error when the location request cannot be fulfilled."""
	def __init__(self, nameInRFC, message=None, **kwargs):
		super(HELD_Error, self).__init__(message)
		self.code = nameInRFC
	def __str__(self):
		return "HELD " + self.__class__.__name__ + (": " + self.message if self.message != None else "")
	
	def pickle_XML(self, serverInfo, *args, **kwargs):
		errorTag = lxml.etree.QName("urn:ietf:params:xml:ns:geopriv:held", "error")
		langAttr = lxml.etree.QName("http://www.w3.org/XML/1998/namespace", "lang")
		errorElem = lxml.etree.Element(errorTag, attrib={"code":self.code})
		msgElem = lxml.etree.Element("message", attrib={langAttr:"en"})
		if self.message != None:
			msgElem.text = self.message
		errorElem.append(msgElem)
		return msgElem

class HELD_Error_Request(Cucumbers.Request, HELD_Error):
	def __init__(self, *args, **kwargs):
		if len(args) >= 1:	kwargs["nameInRFC"] = args[0]
		if len(args) >= 2:	kwargs["message"] = args[1]
		super(HELD_Error_Request, self).__init__(**kwargs)
class HELD_Error_Response(Cucumbers.Response, HELD_Error):
	def __init__(self, *args, **kwargs):
		if len(args) >= 1:	kwargs["nameInRFC"] = args[0]
		if len(args) >= 2:	kwargs["message"] = args[1]
		super(HELD_Error_Request, self).__init__(**kwargs)

class RequestError(HELD_Error_Request, HELD_Error):
	"""Indicates that the request was badly formed in some fashion (other than the XML content)."""
	def __init__(self, unrecognizedLocationType=None):
		msg = "Badly formed request"
		if unrecognizedLocationType:
			msg += ": '" + unrecognizedLocationType + "' locationType not recognized"
		super(RequestError, self).__init__("requestError", msg)
		self.unrecognizedLocationType = unrecognizedLocationType

class XML_Error(HELD_Error_Request, HELD_Error):
	"""Indicates that the XML content of the request was either badly formed or invalid."""
	def __init__(self, extraMsg=None):
		msg = "XML parse error in request"
		if extraMsg:
			msg += ": " + extraMsg
		super(XML_Error, self).__init__("xmlError", msg)

class UnsupportedMessage(HELD_Error_Request, HELD_Error):
	"""
	Indicates that an element in the XML document for the request was not supported or understood.
	
	This error code is used when a HELD request contains a document element that is not supported by the receiver.
	"""
	def __init__(self):
		super(UnsupportedMessage, self).__init__("unsupportedMessage", "Unsupported request")

class GeneralLISError(HELD_Error_Response):
	"""Indicates that an unspecified error occurred at the LIS."""
	def __init__(self):
		super(GeneralLISError, self).__init__("generalLisError", "Unspecified error")

class LocationUnknown(HELD_Error_Response):
	"""
	Indicates that the LIS could not determine the location of the device.
	
	The same request can be sent by the Device at a later time. Devices MUST limit any attempts to retry requests.
	"""
	def __init__(self):
		super(LocationUnknown, self).__init__("locationUnknown", "Location unknown")

class Timeout(HELD_Error_Response):
	"""
	Indicates that the LIS could not satisfy the request within the time specified.
	
	Time specified is in the "responseTime" parameter.
	"""
	def __init__(self):
		super(Timeout, self).__init__("timeout", "Timed out while retrieving location")

class CannotProvideLIType(HELD_Error_Response):
	"""
	Indicates that the LIS was unable to provide LI of the type or types requested.
	
	This code is used when the "exact" attribute on the "locationType" parameter is set to "true".
	"""
	def __init__(self):
		super(CannotProvideLIType, self).__init__("cannotProvideLiType", "Unable to provide type of location requested")

class NotLocatable(HELD_Error_Response):
	"""
	Indicates that the LIS is unable to locate the Device.
	
	The Device MUST NOT make further attempts to retrieve LI from this LIS. This error code is used to indicate
	that the Device is outside the access network served by the LIS, for instance, in a VPN or NAT scenario.
	"""
	def __init__(self):
		super(NotLocatable, self).__init__("notLocatable", "Timed out while retrieving location")
