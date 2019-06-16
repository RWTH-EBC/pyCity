#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
pyCity: Python package for data handling and scenario generation of
city districts.

The MIT License

Copyright (C) 2015-2019  Thomas Schuetz, Jan Schiefelbein

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from setuptools import setup, find_packages

import io
import codecs
import os
import sys


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

#long_description = read('README.md')


setup(name='pycity_base',
      version='0.1',
      description='Python package for data handling and scenario generation '
                  'of city districts.',
      #long_description=long_description,
      long_description='Python package for data handling and scenario generation '
                    'of city districts.',
      url='https://github.com/RWTH-EBC/pyCity',
      author='Institute of Energy Efficient Buildings and Indoor Climate, '
             'Institute for Automation of Complex Power Systems'
             'E.ON Energy Research Center, RWTH Aachen University',
      author_email='pycity@eonerc.rwth-aachen.de',
      license='MIT License',
      packages=['pycity_base'],
      setup_requires=['numpy', 'matplotlib', 'pandas', 'pytest', 'xlrd',
                      'networkx', 'richardsonpy', 'uesgraphs'],
      install_requires=['numpy', 'matplotlib', 'pandas', 'pytest', 'xlrd',
                        'networkx', 'richardsonpy', 'uesgraphs'],
      tests_require=['pytest'],
      platforms='any',
	  classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
		  'Natural Language :: English',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering',
          'Topic :: Utilities']
      )

