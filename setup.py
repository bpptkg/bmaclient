#!/usr/bin/env python

import os

from setuptools import setup


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

setup(
    name='bmaclient',
    version='0.0.1',
    description='BPPTKG Monitoring API Client',
    long_description=read('README.md'),
    license='MIT',
    install_requires=['httplib2', 'six'],
    author='Indra Rudianto',
    author_email='indrarudianto.official@gmail.com',
    url='http://gitlab.com/bpptkg/bmaclient',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Operating System :: POSIX :: Linux',
        'Intended Audience :: Science/Research',
        'Natural Language :: Indonesian',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
