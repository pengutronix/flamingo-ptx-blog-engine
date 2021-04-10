#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    include_package_data=True,
    name='flamingo-ptx-blog-engine',
    version='0.0',
    author='',
    url='',
    author_email='',
    license='',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4==4.5.3',
    ],
    scripts=[
        'bin/flamingo-ptx-blog-new',
    ],
)
