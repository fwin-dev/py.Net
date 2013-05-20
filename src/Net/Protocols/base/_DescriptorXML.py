from _Descriptor import _Descriptor

import lxml.etree
from abc import abstractmethod

class DescriptorXML(_Descriptor):
	"""Same as Descriptor, but lxml documents can be used instead of file-like objects."""
	
	def pickle(self, cucumbers, serverInfo, *args, **kwargs):
		responseFileObj = self._makeContentObj(encoding=self._pickle_XML_getOptions()["encoding"])
		responseXML = self.pickle_XML(cucumbers, serverInfo, *args, **kwargs)
		responseFileObj.write(lxml.etree.tostring(responseXML, **self._pickle_XML_getOptions()))
		return responseFileObj
	
	@abstractmethod
	def pickle_XML(self, cucumbers, serverInfo, *args, **kwargs):
		pass
	
	@classmethod
	def _pickle_XML_getOptions(cls):
		"""These options get passed to lxml.etree.tostring. Must contain at least "encoding" key."""
		return {"encoding": "utf-8"}
	
	def unpickle(self, fileObj, clientInfo, parentCucumbers, *args, **kwargs):
		fileObj.seek(0)
		xmlRoot = lxml.etree.parse(fileObj, **self._unpickle_XML_getOptions())
		return self.unpickle_XML(xmlRoot, clientInfo, parentCucumbers, *args, **kwargs)
	
	@abstractmethod
	def unpickle_XML(self, xmlEtree, clientInfo, parentCucumbers, *args, **kwargs):
		"""
		See super unpickle.
		
		xmlEtree	--- An lxml ElementTree containing all data.
		"""
		pass
	
	@classmethod
	def _unpickle_XML_getOptions(cls):
		"""These options get passed to lxml.etree.parse."""
		return {"parser": lxml.etree.XMLParser(),
				"base_url": None}
