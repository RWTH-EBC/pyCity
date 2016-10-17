<snippet>
  <content>
# pyCity

Python package for data handling and scenario generation of city districts.

# Contributing

1. Clone repository: `git clone git@github.com:RWTH-EBC/pyCity.git` (for SSH usage)
2. Open an issue at [https://github.com/RWTH-EBC/pyCity/issues](https://github.com/RWTH-EBC/pyCity/issues)
3. Checkout development branch: `git checkout development` 
4. Update local development branch (if necessary): `git pull origin development`
5. Create your feature branch: `git checkout -b issueXY_explanation`
6. Commit your changes: `git commit -am 'Add some feature (#XY)'`
7. Push to the branch: `git push origin issueXY_explanation`
8. Submit a pull request from issueXY_explanation to development branch via [https://github.com/RWTH-EBC/pyCity/pulls](https://github.com/RWTH-EBC/pyCity/pulls)

# Installation

pyCity requires the following Python packages:
- numpy
- matplotlib
- pandas
- pytest
- xlrd
- shapely

as well as the python package

- uesgraphs (and its dependencies shapely, pyproj, 'cmocean', 'iapws')

which is available under [https://github.com/RWTH-EBC/uesgraphs](https://github.com/RWTH-EBC/uesgraphs)

### Instructions for uesgraphs and pyCity

First, you should download and install uesgraph. Local installation is possible via pip:

`pip install -e 'your_path_to_uesgraphs_setup'`

Second, you can install pyCity via pip:

`pip install -e 'your_path_to_pycity_setup'`

In case you are using different Python distributions on your machine and your currently used distribution is not in the Python path, 
you can open a Python command window within your Python path (e.g. Winpython cmd window) and type

`python`

and press enter to open the python environment (the Python version number should be shown within cmd prompt).
Then type

`import pip`

enter, then type

`exit()`

and press enter to exit the Python environment. Then you should be able to install the missing Python packages locally to your specific Python distribution
via pip, e.g.

`pip install -e 'your_path_to_uesgraph_setup'`

You can check if installation / adding packages to python has been successful
by adding new .py file and trying to import uesgraphs and pyCity.

`import uesgraphs`

`import pycity`

Import should be possible without errors.

### Instructions for shapely

shapely is required for uesgraphs and pycity usage. A pre-compiled version of shapely for Windows (Windows Binaries for Python Extension Packages) 
can be found at: [http://www.lfd.uci.edu/~gohlke/pythonlibs/](http://www.lfd.uci.edu/~gohlke/pythonlibs/)

Download shapely (version according to your system and Python version, such as 64 bit and Python 3.4)

open a Python command window within your Python path (e.g. Winpython cmd window).
Install the wheel files with pip. 

`pip install SomePackage-1.0-py2.whl`

# Tutorial

pyCity has a jupyter notebook tutorial script under pycity/examples/tutorials/... 
To open the jupyter notebook, open a command/terminal window and change your directory to the directory, 
where tutorial_pycity.ipynb is stored. Then type 'jupyter notebook' (without '' signs) and press Enter.
Jupyter notebook should open within your browser (such as Firefox). Click on one notebook to start.

# License

pyCity is released by RWTH Aachen University's Institute for Energy Efficient Buildings and Indoor Climate (EBC) 
under the [MIT License](https://opensource.org/licenses/MIT)

# Acknowledgements

We gratefully acknowledge the financial support for parts of pyCity by BMWi (German Federal Ministry for Economic Affairs and Energy)

 </content>
</snippet>