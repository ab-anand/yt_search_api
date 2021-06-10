#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from setuptools import setup, find_packages
from yt_search_api.version import VERSION

__version__ = VERSION


if sys.version_info[:2] <= (2, 7):
    with open("README.rst") as f:
        long_description = f.read()
else:
    with open("README.rst", encoding="utf8") as f:
        long_description = f.read()


setup(
    name='yt_search_api',
    author='Abhinav Anand',
    version=VERSION,
    author_email='abhinavanand1905@gmail.com',
    description="A lightweight module to perform a Youtube search",
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/ab-anand/yt_search_api',
    license='MIT',
    install_requires=[
        "pathlib >= 1.0.1",
        "setuptools >= 44.1.1",
        "requests >= 2.25.1"
    ],
    # dependency_links=dependency_links,
    # adding package data to it
    packages=find_packages(exclude=['contrib', 'docs']),
    download_url='https://github.com/ab-anand/yt_search_api/tarball/' + __version__,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.8",
        "Topic :: System",
        "Topic :: System :: Operating System",
        "Topic :: Utilities",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
    ],
    keywords=['Youtube', 'search', 'Automation', 'api']
)