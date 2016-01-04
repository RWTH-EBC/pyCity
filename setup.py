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
      install_requires=['numpy', 'pandas', 'sympy', 'pytest', 'xlrd'],
      cmdclass={'test': PyTest})
