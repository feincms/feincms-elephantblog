#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
import os

import elephantblog


setup(name='feincms-elephantblog',
    version=elephantblog.__version__,
    description='A blog for FeinCMS',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read().decode('utf-8'),
    author='Simon Bächler',
    author_email='sb@feinheit.ch',
    url='https://github.com/sbaechler/feincms-elephantblog/',
    license='BSD License',
    platforms=['OS Independent'],
    packages=[
        'elephantblog',
        'elephantblog.extensions',
        'elephantblog.management.commands',
        'elephantblog.templatetags',
        ],
    )
