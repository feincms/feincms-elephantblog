#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

import elephantblog


setup(
    name="feincms-elephantblog",
    version=elephantblog.__version__,
    description="A blog for FeinCMS",
    long_description=open(os.path.join(os.path.dirname(__file__), "README.rst")).read(),
    author="Simon Baechler",
    author_email="sb@feinheit.ch",
    url="https://github.com/feincms/feincms-elephantblog/",
    license="BSD License",
    platforms=["OS Independent"],
    packages=find_packages(exclude=[],),
    include_package_data=True,
    install_requires=["Django>=1.11", "FeinCMS>=1.15"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    zip_safe=False,
)
