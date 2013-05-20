from Net.Protocols import base
from Lang.Struct import OrderedSet
import lxml
from abc import ABCMeta, abstractmethod

class HELD_Cucumber(base.Cucumber):
	pass

class Response(HELD_Cucumber, base.Cucumber.Response):
	__metaclass__ = ABCMeta
	@abstractmethod
	def pickle_XML(self, *args, **kwargs):
		pass

class Request(HELD_Cucumber, base.Cucumber.Request):
	def __init__(self, locationTypes, locationTypes_areExact):
		super(Request, self).__init__()
		self.locationTypes = locationTypes
		"""An OrderedSet containing expected location response types."""
		self.locationTypes_areExact = locationTypes_areExact
		"""If exact, server must return error if location of that type can't be found. Otherwise, return a different type."""

class LocationURI_set(Response, OrderedSet):
	def __init__(self, expires=None, uri=None):
		"""
		expires	--- A datetime instance with no timezone.
		"""
		self.expires = expires
		assert self.expires.utcoffset() == None
		if uri != None:
			self.append(uri)
	
	def pickle_XML(self, *args, **kwargs):
		elem = lxml.etree.Element("locationUri", attrib={"expires": self.expires.isoformat() + "Z"})
		for locationURI in self:
			elem.append(locationURI.pickle_XML())

class LocationURI(base.LocationURI):
	def pickle_XML(self, *args, **kwargs):
		elem = lxml.etree.Element("locationURI")
		elem.text = str(self)
		return elem
