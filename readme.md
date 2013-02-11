Package description	{#mainpage}
===================

# Summary of functionality

This is a small package of general network/internet related useful things, including:

- Handling IP addresses
- Downloading the latest versioned file from a standard Apache HTTP index page

# Detailed functionality

## IP addresses

This package uses `netaddr` for handling IP addresses. Documentation for that can be found at http://pythonhosted.org/netaddr/

For parsing IPs from strings, use:

	IPaddress.parseString()

See the source of IPaddress.py for more details on everything.

## Downloading a file from an HTTP index page

Requirements:

- The index page must be a standard Apache index page
- The file naming scheme must be name-version.ext where version is something can be alphabetically sorted by python's built-in distutils.version.LooseVersion

For example, to find the latest EPEL release package URL from the following index URL, use:

	from HTTPIndex_FindLatestFile import findLatestFile
	url = findLatestFile("http://dl.fedoraproject.org/pub/epel/6/i386/", "epel-release")
