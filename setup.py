# coding=utf-8
"""
    PyCity: Python package for data handling and scenario generation of
    city districts.
    Copyright (C) 2016  Thomas Schütz, Jan Schiefelbein

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
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


setup(name='pycity',
      version='0.1.0',
      description='Python package for data handling and scenario generation of city districts.',
      url='https://github.com/RWTH-EBC/pyCity',
      author='Thomas Schuetz, Jan Schiefelbein',
      author_email='tschuetz@eonerc.rwth-aachen.de',
      license='GNU General Public License',
      packages=['pycity'],
      install_requires=['numpy', 'pandas', 'sympy', 'pytest', 'xlrd', 'uesgraphs'],
      cmdclass={'test': PyTest})
