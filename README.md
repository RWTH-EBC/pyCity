<snippet>
  <content>
## PyCity

Python package for data handling and scenario generation of city districts.

## Contributing

1. Clone repository: `git clone https://github.com/RWTH-EBC/pyCity.git`
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request

## Installation

PyCity requires the following Python packages:
- numpy
- matplotlib
- pandas
- pytest
- xlrd
- shapely (due to uesgraphs usage)

as well as the python package

- uesgraphs (and its dependencies shapely, pyproj, 'cmocean', 'iapws')

which is available under [https://github.com/RWTH-EBC/uesgraphs](https://github.com/RWTH-EBC/uesgraphs)

First, you should download and install uesgraph. Local installation is possible via pip:

`pip install -e 'your_path_to_uesgraphs_setup'`

Second, you can install pycity via pip:

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
by adding new .py file and trying to import uesgraphs and pycity.

`import uesgraphs`

`import pycity`

Import should be possible without errors.

## Tutorial

PyCity has a jupyter notebook tutorial script under pycity/examples/tutorials/... 
To open the jupyter notebook, open a command/terminal window and change your directory to the directory, 
where tutorial_pycity.ipynb is stored. Then type 'jupyter notebook' (without '' signs) and press Enter.
Jupyter notebook should open within your browser (such as Firefox). Click on one notebook to start.

## License

PyCity is released by RWTH Aachen University's Institute for Energy Efficient Buildings and Indoor Climate (EBC) 
under the [GNU General Public License](http://www.gnu.org/licenses/gpl.html)

## Acknowledgements

We gratefully acknowledge the financial support for parts of PyCity by BMWi (German Federal Ministry for Economic Affairs and Energy)

 </content>
</snippet>