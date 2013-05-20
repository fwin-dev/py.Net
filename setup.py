from setuptools import setup, find_packages

import sys
if sys.version_info[0] >= 3 or sys.version_info <= (2,5):
	raise Exception("This module only supports Python 2.6 or 2.7")

setup(
	name = "py.Net",
	version = "0.5.4",
	description = "Useful classes for common network related functions and abstraction",
	author = "Jesse Cowles",
	author_email = "jcowles@indigital.net",
	url = "http://projects.indigitaldev.net/py.Net",
	
	namespace_packages = ["Net"],
	package_dir = {"":"src"},
	packages = find_packages("src"),
	zip_safe = False,
	install_requires = [
		"netaddr",
		"py.Lang",
	],
	classifiers = [
		# http://pypi.python.org/pypi?%3Aaction=list_classifiers
		"Development Status :: 5 - Production/Stable",
		"Programming Language :: Python :: 2.6",
		"Programming Language :: Python :: 2.7",
		"Operating System :: OS Independent",
	],
)
