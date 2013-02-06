import sys
import OS, OS.pkg

try:
    import iptc
except ImportError:
    OS.pkg.install("iptables")
    from tempfile import mkdtemp
    import urllib, tarfile
    filename, headers = urllib.urlretrieve("https://github.com/ldx/python-iptables/tarball/master")
    file = tarfile.open(filename)
    tmpFolder = mkdtemp(suffix="py_iptables")
    file.extractall(tmpFolder)
    file.close()
    iptc.

class Services:
    @classmethod
    def hasRule(cls, port, policy, proto="tcp", source="0/0", dest="0/0", states=[]):
        if not isinstance(port, list):
            port = list(port)
        policy = policy.upper()
        assert policy in ["ACCEPT", "DROP"]
        
        proto = proto.lower()
        if not isinstance(proto, list):
            proto = list(proto)
        
        states = [state.upper() for state in states]
        if not isinstance(states, list):
            states = list(states)
        
        if source == ["anywhere"]:
            source = ["0/0"]
        if dest == ["anywhere"]:
            dest = ["0/0"]
        
        if proto != ["all"]:
            proto = [proto, "all"]
        
        for line in OS.runCMD("sudo iptables -L").stdout:
            line = line.split()
            if line[0] == policy and line[1] in proto and line[3] == 
            
        sshFinder = lambda x: x[0] == "ACCEPT" and x[1] in ["tcp", "all"] and x[3] == "anywhere" and x[4] == "anywhere" and "dpt:ssh" in x[5:]
    
    @classmethod
    def addRule(cls, port, proto="tcp", source="0/0", dest="0/0", states=None):
    
    @classmethod
    def 
