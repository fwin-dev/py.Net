from setuptools import setup, find_packages

import sys
if sys.version_info[0] == 3 or sys.version_info <= (2,5):
	raise Exception("This module only supports Python 2.6 or 2.7")

setup(
    name = "py.Net",
    version = "0.5.0",
    description = "Contains useful classes for common network related functions and abstraction.",
    author = "Jesse Cowles",
    author_email = "jcowles@indigital.net",
	url = "http://projects.indigitaldev.net/py.Net",
	
	namespace_packages = ["Net"],
	package_dir = {"":"src"},
	packages = find_packages("src"),
    zip_safe = False,
	install_requires = [
		"netaddr",
	],
#	dependency_links = ["http://projects.indigitaldev.net/master#egg=py.OS-0.5.0"],
)
