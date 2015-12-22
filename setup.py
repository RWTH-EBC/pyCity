from setuptools import setup

setup(name='pycity',
      version='0.1.0',
      description='Python package for data handling and scenario generation of city districts.',
      url='https://github.com/RWTH-EBC/pyCity',
      author='Thomas Schuetz, Jan Schiefelbein',
      author_email='tschuetz@eonerc.rwth-aachen.de',
      license='GNU General Public License',
      packages=['pycity'],
      setup_requires = ['numpy', 'pandas', 'sympy', 'xlrd'],
      install_requires = ['numpy', 'pandas', 'sympy', 'xlrd'])