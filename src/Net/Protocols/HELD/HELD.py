from Errors import HELD_Error, XML_Error, GeneralLISError, RequestError
import Cucumbers

from Net.Protocols.PIDF_LO import PIDF_LO
from Net.Protocols.HTTP import HTTP_Interface_Server
from Net.Protocols import base

from Lang.Struct import OrderedSet

import lxml.etree

"""
Implementation of the HELD protocol in python.

Follows RFC 5985: http://tools.ietf.org/html/rfc5985
Follows RFC 6155, but not all identification types are implemented yet: http://tools.ietf.org/html/rfc6155
@author: Jesse Cowles
"""


class HELD_Descriptor_Server(HTTP_Interface_Server, base.Descriptor_Server):
	_unpickle_allLocTypeCodes = set("geodetic", "civic", "locationuri")	# lowercase
	_heldNS = "urn:ietf:params:xml:ns:geopriv:held"
	
	def __init__(self):
		super(HELD_Descriptor_Server, self).__init__()
	def getMIMEtype(self):
		return "application/held+xml"
	
	def pickle_validateCucumbers(self, cucumbers, *args, **kwargs):
		"""
		Validates cucumbers, which comprise the core body of the response.
		
		Return True if validation went OK, or an error response if not.
		
		cucumbers	--- Must be an iterable with either a single PIDF-LO response, 1 or more URIs,
						or an error response.
		"""
		if not hasattr(cucumbers, "__iter__"):
			cucumbers = (cucumbers,)
		for innerProto in cucumbers:
			if not isinstance(innerProto, Cucumbers.Response):
				return GeneralLISError()
		
		# There can only be up to 1 PIDF_LO response, or 1 error response, or 1 location URI response
		if len(filter(lambda x: isinstance(x, PIDF_LO), cucumbers)) > 1:
			return GeneralLISError()
		if len(filter(lambda x: isinstance(x, Cucumbers.LocationURI_set), cucumbers)) > 1:
			return GeneralLISError()
		if len(filter(lambda x: isinstance(x, HELD_Error))) > 1:
			return GeneralLISError()
		return True
	
	def pickle_XML(self, cucumbers, *args, **kwargs):
		"""
		Gets all of the content in the HELD response as a string.
		
		cucumbers	--- Must be an iterable with either a single PIDF-LO response, 1 or more URIs,
						or an error response.
		"""
		if not hasattr(cucumbers, "__iter__"):
			cucumbers = (cucumbers,)
		
		heldResponse = lxml.etree.Element(lxml.etree.QName(self._heldNS, "locationResponse"))
		for cucumber in cucumbers:
			heldResponse.append(cucumber.pickle_XML())
		return lxml.etree.ElementTree(heldResponse) # create top level element/all contents
	
	def _unpickle_locTypes_asList(self, xmlRoot):
		"""Parse locationType codes from a string. Example: "geodetic civic"."""
		locTypeStr, areExact = self._unpickle_locTypes_asStr(xmlRoot)
		locationTypes = OrderedSet([i.lower() for i in locTypeStr.split()])
		if "any" in locationTypes:
			locationTypes.insertMultiBefore("any", self._unpickle_allLocTypeCodes, updateOnExist=False)
			locationTypes.remove("any")
		for code in locationTypes:
			if code not in self._unpickle_allLocTypeCodes:
				raise RequestError(code)
		return locationTypes, areExact
	
	def _unpickle_locTypes_asStr(self, xmlRoot):
		# Parse locationType element
		locTypeNodes = list(xmlRoot.xpath("/held:locationRequest/held:locationType", namespaces={"held":self._heldNS}))
		locTypeNodes += list(xmlRoot.xpath("//*[local-name() = 'locationType']"))
		if len(locTypeNodes) == 0:	# default case
			locationTypeStr = "any"
			areExact = False
		elif len(locTypeNodes) == 1:
			locationTypeStr = locTypeNodes[0].text
			areExact = locTypeNodes[0].get("exact")
			areExact = areExact if areExact != None else False
			locTypeNodes[0].getparent().remove(locTypeNodes[0])		# remove locationType node from document after parsing
		else:
			raise XML_Error("Too many locationTypes found")
		return locationTypeStr, areExact
	
	def _unpickle_locReqElem(self, xmlRoot):
		locReqNode = xmlRoot.xpath("/held:locationRequest", namespaces={"held":self._heldNS})
		if len(locReqNode) == 0:
			raise XML_Error("locationRequest not found")
		elif len(locReqNode) > 1:
			raise XML_Error("Too many locationRequests found")
		return locReqNode[0]
	
	def _unpickle_innerLocReqNodes(self, locReqNode):
		"""Returns a new XML document to pass on to HELD_ID."""
		if len(locReqNode) > 0:
			newRoot = lxml.etree.Element("root")
			for childNode in locReqNode:
				newRoot.append(childNode)
		else:
			newRoot = None
		return newRoot
	
	def unpickle_XML(self, xmlEtree, *args, **kwargs):
		"""responseTime attribute described in the RFC is ignored."""
		try:
			locReqNode = self._unpickle_locReqElem(xmlEtree)	# check locationRequest XML element exists
			locTypes, locTypes_areExact = self._unpickle_locTypes_asList(xmlEtree)
			requestObj = Cucumbers.Request(locTypes, locTypes_areExact)
			innerBody = self._unpickle_innerLocReqNodes(locReqNode)
			return {"cucumbers": (requestObj,), "innerProtoBody": innerBody, "innerProtoInst": "HELD_ID"}
		except HELD_Error as err:
			return {"cucumbers": (err,), "innerProtoBody": None}
	
	def _unpickle_XML_getOptions(self):
		return {"parser": lxml.etree.XMLParser(ns_clean=True), "base_url": None}

