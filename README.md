![E.ON EBC RWTH Aachen University](./documentation/_static/EBC_Logo.png)


[![Build Status](https://travis-ci.com/RWTH-EBC/pyCity.svg?token=ssfy4ps1Qm5kvs5yAxfm&branch=master)](https://travis-ci.com/RWTH-EBC/pyCity.svg?token=ssfy4ps1Qm5kvs5yAxfm&branch=master)


# pyCity

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

pyCity requires the following Python packages:
- numpy
- matplotlib
- networkX
- pandas
- pytest
- xlrd

as well as the EBC Python packages:

- uesgraphs
(with dependencies to shapely and pyproj)

which is available under 
[https://github.com/RWTH-EBC/uesgraphs](https://github.com/RWTH-EBC/uesgraphs)

and

- richardsonpy 

which is available under [https://github.com/RWTH-EBC/richardsonpy](https://github.com/RWTH-EBC/richardsonpy)

### Installation of uesgraph and its dependencies

If you have not installed uesgraphs and its dependencies yet, you should do 
the uesgraphs installation as first step.

If you are working with Linux or Mac OS, you should be able to directly 
install uesgraphs via pip. Therefore, clone the uesgraphs repository to one 
local folder and install it via pip:

`pip install -e '<your_path_to_uesgraph_setup_folder>'`

The `-e` generates an egglink from your Python distribution to your local
uesgraphs repository.

If you are working with Windows OS, you might run into compiler problems 
when trying to install uesgraphs, as the uesgraphs setup.py tries to install
shapely and pyprof, too. 
As a workaround, you can download precompiled Windows binaries for shapely 
and pyproj from:
[http://www.lfd.uci.edu/~gohlke/pythonlibs/](http://www.lfd.uci.edu/~gohlke/pythonlibs/)

Select the wheel file, which matches your Python installation 
(version e.g. 2.7 or 3.6) (system infrastructure, e.g. 32 bit or 64 bit)

Now you should be able to install the wheel files via pip:

`pip install <path_to_your_shapely_file>\shapely.whl`

`pip install <path_to_your_pyproj_file>\pyproj.whl`

Now you should be able to install uesgraphs via pip:

`pip install -e '<your_path_to_uesgraph_setup_folder>'`

In case the Python path does not point at your Python distribution and you
do not have admin rights (might be the case for some of E.ON ERC students),
you can directly call the Python interpreter of your distribution to install
packages via pip:

`<path_to_your_python_dist\Python.exe> -m pip install <package_name>'`

`<path_to_your_python_dist\Python.exe> -m pip install -e '<your_path_to_local_package_setup_folder>'`

### Installation of pyCity

When uesgraph and its dependencies are installed, you should be able to install
pyCity via pip:

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
