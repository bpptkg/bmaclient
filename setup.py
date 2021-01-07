#!/usr/bin/env python

import io
import os
import re

from setuptools import find_packages, setup

with io.open('bmaclient/version.py', 'rt', encoding='utf-8') as f:
    version = re.search(r"__version__ = '(.*?)'", f.read()).group(1)


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name='bmaclient',
    version=version,
    description='BPPTKG Monitoring API Python Client',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    license='MIT',
    install_requires=[
        'httplib2>=0.9',
        'six>=1.8.0',
    ],
    author='Indra Rudianto',
    author_email='indrarudianto.official@gmail.com',
    url='https://gitlab.com/bpptkg/bmaclient',
    zip_safe=False,
    packages=find_packages(exclude=['tests', 'docs']),
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Operating System :: POSIX :: Linux',
        'Intended Audience :: Science/Research',
        'Natural Language :: Indonesian',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)
