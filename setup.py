#!/usr/bin/env python

import os

from setuptools import setup, find_packages

__version__ = '0.5.0'


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name='bmaclient',
    version=__version__,
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
    zip_safe=True,
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
    ]
)
