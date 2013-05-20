from urlparse import urlparse

class LocationURI(object):
	"""
	Stores a location URI. Attributes should not be modified after instantiation.
	
	See the following for specifications:
	http://en.wikipedia.org/wiki/URI_scheme#Generic_syntax
	http://tools.ietf.org/html/rfc3986
	
	This class is nearly identical to urlparse.ParseResult, with a few differences.
	1. This class does not use "named tuples" which are nearly identical to a dict. It is believed that named tuples
	were created for backwards compatibility with that class, which is being dropped here.
	2. ParseResult is read only, whereas this class could more easily be expanded in the future	to allow writing
	to instance attributes.
	3. This class uses "authority" instead of "netloc" because "authority" is the term used in RFC 3986.
	"""
	def __init__(self, scheme, hostname, username=None, password=None, port=None, path=None, query=None, fragment=None):
		self.scheme = scheme
		self.hostname = hostname
		self.username = username
		self.password = password
		self.port = port
		self.path = path
		self.query = query
		if isinstance(self.query, dict):
			self.query = "&".join((k + "=" + v for k, v in dict.iteritems()))
		self.fragment = fragment
	
	def __str__(self):
		str_ = self.scheme + ":"
		if self.username != None:
			str_ += self.username
			if self.password != None:
				str_ += ":" + self.password
			str_ += "@"
		str_ += self.hostname
		if self.path != None:
			if self.path[0] != "/":
				self.path = "/" + self.path
			str_ += self.path
		if self.query != None:		str_ += "?" + self.query
		if self.fragment != None:	str_ += "#" + self.fragment
		
	
	@classmethod
	def parseStr(cls, uriStr):
		"""Parses a URI from a string."""
		result = urlparse(uriStr)
		dict_ = {}
		for key in ("scheme", "netloc", "path", "query", "fragment", "username", "password", "hostname", "port"):
			dict_[key] = result.key if result.key != "" else None
		return LocationURI(**dict_)
