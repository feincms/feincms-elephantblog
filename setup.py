#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

import elephantblog


setup(name='feincms-elephantblog',
    version=elephantblog.__version__,
    description='A blog for FeinCMS',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read().decode('utf-8'),
    author='Simon Baechler',
    author_email='sb@feinheit.ch',
    url='https://github.com/feincms/feincms-elephantblog/',
    license='BSD License',
    platforms=['OS Independent'],
    packages=find_packages(),
    include_package_data=True
    )
