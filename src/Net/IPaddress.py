# http://packages.python.org/netaddr/tutorial_01.html

from netaddr import IPNetwork as Subnet
from netaddr import IPGlob as Glob
from netaddr import IPRange as Range
from netaddr import IPAddress as Host

def parseString(address, acceptMultiple=True, returnStr=False):
	"""
	@param address			str:	See below
	@param acceptMultiple	str:	If `False` and multiple IPs are specified, raise an exception
	@param returnStr		bool:	If `True`, return addresses as strings. If `False`, return Host instances.
	
	Address can be:
	A subnet (192.168.0.1/24)
	A dashed range (192.168.0.1-192.168.0.7)
	A glob range (192.168.0.*)
	A single host (192.168.0.1)
	"""
	
	addrs = []
	if address.find("/") != -1:
		assert acceptMultiple
		addrs = [i for i in Subnet(address).iter_hosts()]
	elif address.find("-") != -1:
		assert acceptMultiple
		addrs = [i for i in Range(*(address.split("-")))]
	elif address.find("*") != -1:
		assert acceptMultiple
		addrs = [i for i in Glob(address)]
	else:
		addrs = [Host(address)]
	
	if returnStr:
		return [str(i) for i in addrs]
	else:
		return addrs
