#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="shortcats",
    version="0.1",
    url="http://github.com/mapleoin/shortcats",
    author="Ionuț Arțăriși",
    author_email="ionut@artarisi.eu",
    long_description=__doc__,
    packages=find_packages(exclude=["*.test", "test", "*.test.*"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask'],
    test_suite="shortcats.tests"
    )
