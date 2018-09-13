![E.ON EBC RWTH Aachen University](./doc/_static/EBC_Logo.png)


[![Build Status](https://travis-ci.com/RWTH-EBC/pyCity.svg?token=ssfy4ps1Qm5kvs5yAxfm&branch=master)](https://travis-ci.com/RWTH-EBC/pyCity.svg?token=ssfy4ps1Qm5kvs5yAxfm&branch=master)
[![License](http://img.shields.io/:license-mit-blue.svg)](http://doge.mit-license.org)


# pyCity_base

Python package for data handling and scenario generation of city districts.

## Contributing

1. Clone repository: `git clone git@github.com:RWTH-EBC/pyCity.git` (for SSH usage)
Alternatively: Clone via https: `git clone https://github.com/RWTH-EBC/pyCity.git`
2. Open an issue at [https://github.com/RWTH-EBC/pyCity/issues](https://github.com/RWTH-EBC/pyCity/issues)
3. Checkout development branch: `git checkout development` 
4. Update local development branch (if necessary): `git pull origin development`
5. Create your feature branch: `git checkout -b issueXY_explanation`
6. Commit your changes: `git commit -m "Add some feature #XY"`
7. Push to the branch: `git push origin issueXY_explanation`
8. Submit a pull request from issueXY_explanation to development branch via [https://github.com/RWTH-EBC/pyCity/pulls](https://github.com/RWTH-EBC/pyCity/pulls)

## Installation

*One important issue at the beginning: Please do NOT confuse pyCity_base with
the pycity package on pypi! This (other) pycity package is installable via 
pip. However, if you want to install pycity_base, follow this instruction.*

pyCity_base requires the following Python packages:
- numpy
- matplotlib
- networkX
- pandas
- pytest
- xlrd

as well as the EBC Python packages:

- richardsonpy 

which is available under [https://github.com/RWTH-EBC/richardsonpy](https://github.com/RWTH-EBC/richardsonpy)

- uesgraphs
(with dependencies to shapely and pyproj)

which is available under 
[https://github.com/RWTH-EBC/uesgraphs](https://github.com/RWTH-EBC/uesgraphs)

richardsonpy can be installed via pip.
uesgraphs can be installed via pip on Linux or Mac OS distributions.
In contrast, uesgraphs installation might not be possible via pip on Windows
machines, due to compiler issues with the dependencies to shapely and pyproj.
In this case, follow the instructions of the uesgraphs installation:
[https://github.com/RWTH-EBC/uesgraphs/blob/master/README.md](https://github.com/RWTH-EBC/uesgraphs/blob/master/README.md)
(see Install uesgraphs)

### Installation of pyCity_base

When uesgraph and its dependencies are installed, you should be able to install
pyCity_base via pip:

`pip install -e '<your_path_to_pycity_setup_folder>'`

`<path_to_your_python_dist\Python.exe> -m pip install -e '<your_path_to_pycity_setup_folder>'`

You can check if installation / adding packages to python has been successful
by adding new .py file and trying to import uesgraphs and pyCity.

`import uesgraphs`

`import pycity_base`

Import should be possible without errors.



## Tutorial

pyCity has a jupyter notebook tutorial script under pycity/examples/tutorials/... 
To open the jupyter notebook, open a command/terminal window and change your directory to the directory, 
where tutorial_pycity_calc_1.ipynb is stored. Then type 'jupyter notebook' (without '' signs) and press Enter.
Jupyter notebook should open within your browser (such as Firefox). Click on one notebook to start.
If your Pyhton path does not point at your Python installation, you have to
open jupyter notebook directly, e.g. by looking for the jupyter.exe in your distribution.

## License

pyCity is released by RWTH Aachen University's E.ON Energy Research Center (E.ON ERC),
Institute for Energy Efficient Buildings and Indoor Climate (EBC) and
Institute for Automation of Complex Power Systems (ACS)
under the [MIT License](https://opensource.org/licenses/MIT)

## Acknowledgements

We gratefully acknowledge the financial support by BMWi 
(German Federal Ministry for Economic Affairs and Energy) 
under promotional references 03ET1138D and 03ET1381A.

<img src="http://www.innovation-beratung-foerderung.de/INNO/Redaktion/DE/Bilder/Titelbilder/titel_foerderlogo_bmwi.jpg;jsessionid=4BD60B6CD6337CDB6DE21DC1F3D6FEC5?__blob=poster&v=2)" width="200">
