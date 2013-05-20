from abc import ABCMeta, abstractmethod

class _Descriptor(object):
	__metaclass__ = ABCMeta
	
	def pickle_validateCucumbers(self, cucumbers, *args, **kwargs):
		"""
		Validates cucumbers, which comprise the core body of the response. Implementation is optional.
		
		cucumbers	--- An iterable of instances of the type returned by the associated getInterfaceClass method.
		
		Return True if validation went OK, or an exception if not. Do not raise the exception; just return it.
		"""
		return True
	
	@classmethod
	def _makeContentObj(cls, encoding="utf-8"):
		import StringIO, codecs
		codecinfo = codecs.lookup(encoding)
		return codecs.StreamReaderWriter(StringIO.StringIO(), codecinfo.streamreader, codecinfo.streamwriter)
	
	@classmethod
	def _pickle_joinCucumbers(cls, cucumbers, encoding="utf-8"):
		"""Combines all cucumbers into one file-like object, returning it. No need to seek(0)."""
		# join all inner responses (PIDF-LO, URI, etc.)
		if not hasattr(cucumbers, "__iter__"):
			cucumbers = (cucumbers,)
		pickledBody_all = cls._makeContentObj(encoding)
		for innerProto in cucumbers:
			pickledBody = innerProto.pickle()
			pickledBody.seek(0)
			pickledBody_all.write(pickledBody.read())
			pickledBody.close()
		pickledBody_all.seek(0)
		return pickledBody_all
	
	@abstractmethod
	def pickle(self, cucumbers, innerProtoBody, innerProtoInst, serverInfo, *args, **kwargs):
		"""
		Converts (a series of) python objects to a file-like object.
		
		cucumbers		--- An single or iterable of instances of the type returned by the associated getInterfaceClass
							method. Can also be None.
		innerProtoBody	--- If an innerProto ProtocolDescriptor was used before this one, this argument contains the
							file-like object which was created by the innerProto. Otherwise, this is None.
		innerProtoInst	--- If an innerProto ProtocolDescriptor was used before this one, this argument contains the
							instance of that innerProto. Otherwise, this is None.
		serverInfo		--- TODO
		
		Returns a dict with the following keys and values:
			fileObj			--- The file-like object written to by this method containing the pickled data.
			outerProtoInst	--- If the current (inner) protocol is unaware of a required outer protocol, or if there
								can be no outer protocol for some reason, or if multiple immediate outer protocols are
								possible, or if the outer protocol is optional, this key should not exist in the
								returned dictionary. Otherwise, the value associated with this key should be an
								instance of a ProtocolDescriptor whose pickle method will be called next.
		"""
		pass
	
	@abstractmethod
	def unpickle(self, fileObj, clientInfo, parentCucumbers, *args, **kwargs):
		"""
		Converts the file-like object using this protocol to (a number of) python objects.
		
		fileObj			--- File-like object containing request. Must seek(0) before reading.
		clientInfo		--- ClientInfo object containing properties about the client/server which sent the content in
							fileObj. Must have a property named 'IP' containing the IP address.
		parentCucumbers	--- OrderedDict	--- Cucumbers unpickled so far from other (parent) protocols. Last element
											will contain the immediate parent. First element will contain the first,
											most distant parent.
		
		Returns a dict with the following keys and values:
			cucumbers		--- A list of all python objects created by this method.
			innerProtoBody	--- Contains a file-like object of inner content/body which cannot be unpickled by this
								protocol, and instead must be unpickled by the next inner protocol. If there is no
								unprocessed inner content, this value should be None.
			innerProtoInst	--- The protocol descriptor instance which will handle the innerProtoBody. If there is
								no unprocessed inner content, this key need not exist. If the PickleMaster should
								determine the next protocol based on a predefined class, make this value None.
		"""
		pass


class Descriptor_Client(_Descriptor):
	pass
class Descriptor_Server(_Descriptor):
	pass
