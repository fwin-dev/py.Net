import os, os.path, sys

def installPyGitProject(pyPackageName, gitProjectName, serverIP):
	# centos based machines don't usually have /usr/local/lib/python
	localLibPath = "python" + str(sys.version_info[0]) + "." + str(sys.version_info[1])
	localLibPath = os.path.join("/usr/local/lib/", localLibPath, "dist-packages")
	if localLibPath not in sys.path:
		sys.path.append(localLibPath)
	
	import shlex
	from subprocess import Popen
	
	print("Warning: Could not find " + pyPackageName + ". Attempting to git clone...")
	proc = Popen(shlex.split("apt-get -y install git"))
	if proc.wait() != 0:
		proc = Popen(shlex.split("yum -y install git"))
		if proc.wait() != 0:
			sys.exit("Could not install git")
	
	fullPyPath = os.path.join(localLibPath, pyPackageName)
	os.makedirs(fullPyPath)
	gitCMD = "git clone git@" + serverIP + ":/" + gitProjectName + " " + fullPyPath
	proc = Popen(shlex.split(gitCMD))
	result = proc.wait()
	if result != 0:
		sys.exit("Error: Could not find or git clone " + pyPackageName)
	print("Notice: Installed " + pyPackageName)
