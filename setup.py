# coding=utf-8
"""
pyCity: Python package for data handling and scenario generation of
city districts.

The MIT License

Copyright (C) 2015-2017  Thomas Schütz, Jan Schiefelbein

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


from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

import pycity

here = os.path.abspath(os.path.dirname(__file__))


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


setup(name='pyCity',
      version='0.1.0',
      description='Python package for data handling and scenario generation of city districts.',
      url='https://github.com/RWTH-EBC/pyCity',
      author='Thomas Schuetz, Jan Schiefelbein',
      author_email='tschuetz@eonerc.rwth-aachen.de',
      license='MIT License',
      packages=['pycity'],
	  setup_requires=['numpy', 'pandas', 'pytest', 'xlrd', 'uesgraphs', 'shapely'],
      install_requires=['numpy', 'pandas', 'pytest', 'xlrd', 'uesgraphs', 'shapely'],
      cmdclass={'test': PyTest})
