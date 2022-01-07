#!/usr/bin/env python

import os

from setuptools import find_packages, setup

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
    packages=find_packages(
        exclude=[],
    ),
    include_package_data=True,
    install_requires=["Django>=3.2", "FeinCMS>=1.15"],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    zip_safe=False,
)
