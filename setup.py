#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup
from server_status import __version__

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-server-status',
    version='0.0.1',
    long_description=read('README.md'),
    description='A public components status report app for your Django projects.',
    author='Zenobius Jiricek',
    author_email='airtonix@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    keywords="django health check monitoring",
    classifiers=['Development Status :: 4 - Beta',
                 'Environment :: Web Environment',
                 'Framework :: Django',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Topic :: Utilities'],
    install_requires=[
        'Django>=1.4',
        'setuptools',
    ],
    license='BSD'
)
