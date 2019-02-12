#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 01:56:39 2019

@author: Jamie

Django-database is a django application to manage the MySQL database of Mobitrack.

Detailed documentation is available in the readme.
"""

import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()
    
# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__),os.pardir)))

setup(
      name='django-database',
      version='0.1',
      packages=find_packages(),
      include_package_data=True,
      description='A Django app for Mobitrack database',
      author='Jamie Kim',
      classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.1',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',]
      )