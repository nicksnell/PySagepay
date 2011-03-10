#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sagepay API setup script

from setuptools import setup, find_packages

long_description = """Sagepay API interface

Python interface to the SagePay API. Currently supports:

- Direct Payments (w/ 3D Secure)
- Refunds
- Deferred Payments with Release/Abort
- PayPal Payments
"""

setup(
	name='Sagepay',
	version=1.3,
	description='Sagepay API interface',
	long_description=long_description,
	author='Nick Snell',
	author_email='nick@orpo.co.uk',
	url='http://orpo.co.uk/code/',
	download_url='',
	license='BSD',
	platforms=[],
	classifiers=[
		'Environment :: Web Environment',
		'License :: OSI Approved :: BSD License',
		'Natural Language :: English',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
	],
	zip_safe=True,
	packages=find_packages(exclude=['tests',]),
	dependency_links = [
	
	],
	entry_points = {
	
	},
	install_requires=[
	
	]
)