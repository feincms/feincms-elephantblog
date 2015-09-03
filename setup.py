#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

import elephantblog


setup(
    name='feincms-elephantblog',
    version=elephantblog.__version__,
    description='A blog for FeinCMS',
    long_description=open(
        os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    author='Simon Baechler',
    author_email='sb@feinheit.ch',
    url='https://github.com/feincms/feincms-elephantblog/',
    license='BSD License',
    platforms=['OS Independent'],
    packages=find_packages(
        exclude=[],
    ),
    include_package_data=True,
    install_requires=[
        'Django>=1.7',
        'FeinCMS>=1.11',  # For Django 1.7, 1.10.x would work as well...
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    zip_safe=False,
)
