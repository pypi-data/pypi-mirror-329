#!/usr/bin/env python3
import json
import os
from setuptools import find_namespace_packages
from setuptools import setup


packages = find_namespace_packages(
    exclude={'build', 'dist', 'tests', 'var'}
)
opts = json.loads((open(f'{packages[0]}/package.json').read()))
curdir = os.path.abspath(os.path.dirname(__file__))
version = str.strip(open('VERSION').read())
if os.path.exists(os.path.join(curdir, 'README.md')):
    with open(os.path.join(curdir, 'README.md'), encoding='utf-8') as f:
        opts['long_description'] = f.read()
        opts['long_description_content_type'] = "text/markdown"

setup(
    version=version,
    packages=packages,
    include_package_data=True,
    **opts)
