from descriptor import _Descriptor, Cucumber

from collections import OrderedDict
from copy import copy

class PickleMaster:
	@classmethod
	def pickle(cls, cucumberDict, protoInstList, serverInfo):
		"""
		Creates a serialized file-like object (aka pickles) containing all of the python objects in cucumberDict.
		
		cucumberDict	--- OrderedDict	--- example: {<HTTP descriptor instance>: [<HTTP header obj>, <HTTP body obj>],
													  <HELD descriptor instance>: [<HELD body obj>, ...],
													  <PIDF_LO descriptor instance>: [<PIDF_LO body obj>]}
		"""
		cucumberDict = copy(cucumberDict)
		cucumberDict.reverse()
		cucumberDict_index = 0
		cucumberDict_inst, cucumbers = cucumberDict.items()[cucumberDict_index]
		currentOuterInst = cucumberDict_inst
		
		while currentOuterInst != None:
			isValid = currentOuterInst.pickle_validateCucumbers(cucumbers)
			if isValid == True:
				result = currentOuterInst.pickle(cucumbers, serverInfo)
			elif isinstance(isValid, Exception):
				assert isinstance(isValid, Cucumber)
				result = currentOuterInst.pickle(isValid, serverInfo)
			else:
				raise ValueError("Invalid result from validateCucumbers(...). Must return True or a subclass of Exception and Cucumber.")
			currentOuterBody = result["fileObj"]
			assert hasattr(currentOuterBody, "read")
			
			cucumberDict_index += 1
			if cucumberDict_index < len(cucumberDict):
				cucumberDict_inst, cucumbers = cucumberDict.items()[cucumberDict_index]
			else:
				cucumberDict_inst = cucumbers = None
			
			# verify next outer instance in configuration and the one returned by pickle is the same
			if "outerProtoInst" in result:
				assert isinstance(result["outerProtoInst"], _Descriptor)
				if cucumberDict_inst != None and cucumberDict != result["outerProtoInst"]:
					raise ValueError("Next protocol instance in configuration value (" + str(cucumberDict_inst) + ") does not match what innerProto returned (" + str(currentOuterInst)) + ")"
				currentOuterInst = result["outerProtoInst"]
			elif cucumberDict_inst != None:
				currentOuterInst = cucumberDict_inst
			else:
				currentOuterInst = None
	
	@classmethod
	def unpickle(cls, fileObj, protoInstList, clientInfo):
		"""
		Creates python objects (aka cumcumbers) out of fileObj with the given protocols in protoInstList.
		
		Returns an ordered dict of cucumbers with protocol instances as keys, and objects created by the protocol as values.
		
		protoInstList	--- Ex. (HTTP(), HELD(), PIDF_LO())
		"""
		allCucumbers = OrderedDict()
		currentBody = fileObj
		currentProtoInst_fromListIndex = 0
		currentProtoInst = cls._unpickle_getProtoInstance(protoInstList[currentProtoInst_fromListIndex])
		while currentProtoInst != None:
			currentResult = currentProtoInst.unpickle(currentBody, clientInfo, allCucumbers)
			assert isinstance(currentResult, dict)
			
			assert "cucumbers" in currentResult and hasattr(currentResult["cucumbers"], "__iter__")
			for cucumber in currentResult["cucumbers"]:
				assert isinstance(cucumber, Cucumber)
			allCucumbers[protoInstList] = tuple(currentResult["cucumbers"])
			
			assert "innerProtoBody" in currentResult
			if currentResult["innerProtoBody"] == None:
				currentProtoInst = None
				continue
			
			assert hasattr(currentResult["innerProtoBody"], "read")
			assert "innerProtoInst" in currentResult
			if currentResult["innerProtoInst"] != None:		# _Descriptor class can specify next protocol
				currentProtoInst = cls._unpickle_getProtoInstance(currentResult["innerProtoInst"])
			else:	# next protocol can be specified in protoInstList
				currentProtoInst = cls._unpickle_getProtoInstance(protoInstList[currentProtoInst_fromListIndex])
			
			currentBody = currentResult["innerProtoBody"]
			currentProtoInst_fromListIndex += 1
		
		return allCucumbers
	
	def _unpickle_getProtoInstance(self, unknownProto):
		if isinstance(unknownProto, _Descriptor):
			return unknownProto
		elif issubclass(unknownProto):
			return unknownProto()
		else:
			foundProto = _Descriptor.find(unknownProto)
			assert foundProto != None
			return foundProto

