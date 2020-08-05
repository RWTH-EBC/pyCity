![E.ON EBC RWTH Aachen University](./doc/_static/EBC_Logo.png)


[![Build Status](https://travis-ci.org/RWTH-EBC/pyCity.svg?branch=master)](https://travis-ci.org/RWTH-EBC/pyCity)
[![Coverage Status](https://coveralls.io/repos/github/RWTH-EBC/pyCity/badge.svg)](https://coveralls.io/github/RWTH-EBC/pyCity)
[![License](http://img.shields.io/:license-mit-blue.svg)](http://doge.mit-license.org)


# pycity_base

Python package for data handling and scenario generation of city districts and urban energy systems.

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

*One important issue at the beginning: Please do NOT confuse pycity_base with
the pycity package on pypi! This (other) pycity package is installable via 
pip. However, if you want to install pycity_base, follow this instruction.*

pycity_base requires the following Python packages:
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

### Installation of pycity_base

The latest version of pycity_base is 0.3.0.

When uesgraph and its dependencies are installed, you should be able to install
pycity_base via pip:

`pip install pycity_base`

or:

`pip install -e '<your_path_to_pycity_setup_folder>'`

or:

`<path_to_your_python_dist\Python.exe> -m pip install -e '<your_path_to_pycity_setup_folder>'`


You can check if installation / adding packages to python has been successful
by adding new .py file and trying to import uesgraphs and pyCity.

`import uesgraphs`

`import pycity_base`

Import should be possible without errors.

## Example usage

```Python
import shapely.geometry.point as point
import matplotlib.pyplot as plt

import uesgraphs.visuals as uesvis

import pycity_base.classes.timer as time
import pycity_base.classes.weather as weath
import pycity_base.classes.prices as price
import pycity_base.classes.environment as env
import pycity_base.classes.demand.apartment as apart
import pycity_base.classes.demand.occupancy as occ
import pycity_base.classes.demand.domestic_hot_water as dhw
import pycity_base.classes.demand.electrical_demand as eldem
import pycity_base.classes.demand.space_heating as spaceheat
import pycity_base.classes.building as build
import pycity_base.classes.city_district as citydist
import pycity_base.classes.supply.building_energy_system as besys
import pycity_base.classes.supply.boiler as boil
import pycity_base.classes.supply.photovoltaic as pvsys


def main():
    #  Define the time discretization for the timer object
    timestep = 3600  # in seconds

    #  Define the total number of timesteps (in this case for one year)
    nb_timesteps = int(365 * 24 * 3600 / timestep)

    #  Generate environment with timer, weather, and prices objects
    #  ######################################################################
    timer = time.Timer(timeDiscretization=timestep,
                       timestepsTotal=nb_timesteps)
    weather = weath.Weather(timer=timer)
    prices = price.Prices()

    environment = env.Environment(timer=timer, weather=weather, prices=prices)

    #  Generate city district object
    #  ######################################################################
    city_district = citydist.CityDistrict(environment=environment)
    #  Annotations: To prevent some methods of subclasses uesgraph / nx.Graph
    #  from failing (e.g. '.subgraph()) environment is set as optional input
    #  parameter. However, it is necessary to use an environment object as
    #  input parameter to initialize a working cityDistrict object!

    #  Empty dictionary for building positions
    dict_pos = {}

    #  Generate shapely point positions
    dict_pos[0] = point.Point(0, 0)  # (x, y)
    dict_pos[1] = point.Point(20, 0)

    #  Use for loop to generate two identical building objects for city
    #  district
    #  ######################################################################
    for i in range(2):
        living_area = 200  # in m^2
        spec_sh_dem = 160  # Specific space heating demand in kWh/m^2
        number_occupants = 3  # Total number of occupants

        #  Generate space heating demand object (holding loadcurve attribute
        #  with space heating power)
        heat_demand = spaceheat.SpaceHeating(
            environment=environment,
            method=1,  # Standard load profile
            livingArea=living_area,  # in m^2
            specificDemand=spec_sh_dem)  # in kWh/m^2

        #  Generate occupancy object with stochastic user profile
        occupancy = occ.Occupancy(environment=environment,
                                  number_occupants=number_occupants)

        #  Generate electrical demand object
        el_dem_stochastic = eldem.ElectricalDemand(
            environment=environment,
            method=2,  # stochastic Richardson profile (richardsonpy)
            total_nb_occupants=number_occupants,  # Number of occupants
            randomizeAppliances=True,  # Random choice of installed appliances
            lightConfiguration=10,  # Light bulb configuration nb.
            occupancy=occupancy.occupancy,  # Occupancy profile (600 sec resolution)
            prev_heat_dev=True,  # Prevent space heating and hot water devices
            annualDemand=None,  # Annual el. demand in kWh could be used for
            do_normalization=False)  # rescaling (if do_normalization is True)
        #  Annotation: The calculation of stochastic electric load profiles
        #  is time consuming. If you prefer a faster method, you can either
        #  hand over an own array-like load curve (method=0) or generate a
        #  standardized load profile (SLP) (method=1)

        #  Generate domestic hot water demand object
        dhw_obj = dhw.DomesticHotWater(
            environment=environment,
            tFlow=60,  # DHW output temperature in degree Celsius
            method=2,  # Stochastic dhw profile
            supplyTemperature=25,  # DHW inlet flow temperature in degree C.
            occupancy=occupancy.occupancy)  # Occupancy profile (600 sec resolution)

        #  Generate apartment and add demand curves
        apartment = apart.Apartment(environment)
        apartment.addMultipleEntities([heat_demand,
                                       el_dem_stochastic,
                                       dhw_obj])

        #  Generate building and add apartment
        building = build.Building(environment)
        building.addEntity(apartment)

        #  Add buildings to city district
        city_district.addEntity(entity=building,
                                position=dict_pos[i])

    #  Access information on city district object instance
    #  ######################################################################
    print('Get number of building entities:')
    print(city_district.get_nb_of_building_entities())
    print()

    print('Get list with node ids of building entities:')
    print(city_district.get_list_build_entity_node_ids())
    print()

    print('Get city district overall space heating power load curve:')
    print(city_district.get_aggr_space_heating_power_curve(current_values=True))
    print()
    
    print('Get city district overall space cooling power load curve:')
    print(city_district.get_aggr_space_cooling_power_curve(current_values=True))
    print()

    #  We can use the Visuals class of uesgraphs to plot the city district

    #  Generate uesgraphs visuals object instance
    uesvisuals = uesvis.Visuals(uesgraph=city_district)

    fig = plt.figure()
    ax = fig.gca()
    ax = uesvisuals.create_plot_simple(ax=ax)
    plt.show()
    plt.close()

    #  Access buildings
    #  ######################################################################
    #  As city_district is a networkx graph object, we can access the building
    #  entities with the corresponding building node,
    #  Pointer to building object with id 1001:
    building_1001 = city_district.nodes[1001]['entity']

    print('Get building 1001 electric load curve:')
    print(building_1001.get_electric_power_curve())
    print()

    #  Add energy systems to buildings
    #  ######################################################################
    #  We can also add building energy systems (BES) to each building object

    #  Generate boiler object
    boiler = boil.Boiler(environment=environment,
                         qNominal=10000,  # Boiler thermal power in Watt
                         eta=0.85)  # Boiler efficiency

    #  Generate PV module object
    pv = pvsys.PV(environment=environment,
                  area=30,  # Area in m^2
                  eta=0.15)  # Electrical efficiency at NOCT conditions

    # Instantiate BES (container object for all energy systems)
    bes = besys.BES(environment)

    #  Add energy systems to bes
    bes.addMultipleDevices([boiler, pv])

    #  Add bes to building 1001
    building_1001.addEntity(entity=bes)

    print('Does building 1001 has a building energy system (BES)?')
    print(building_1001.hasBes)

    #  Access boiler nominal thermal power
    print('Nominal thermal power of boiler in kW:')
    print(building_1001.bes.boiler[0].qNominal / 1000)


if __name__ == '__main__':
    #  Run program
    main()

```

## Tutorial

pycity_base also has also a jupyter notebook tutorial script under pycity/examples/tutorials/... 
To open the jupyter notebook, open a command/terminal window and change your directory to the directory, 
where tutorial_pycity_calc_1.ipynb is stored. Then type 'jupyter notebook' (without '' signs) and press Enter.
Jupyter notebook should open within your browser (such as Firefox). Click on one notebook to start.
If your Pyhton path does not point at your Python installation, you have to
open jupyter notebook directly, e.g. by looking for the jupyter.exe in your distribution.

## How to cite pycity_base

+ Schiefelbein, J., Rudnick, J., Scholl, A., Remmen, P., Fuchs, M., Müller, D. (2019),
Automated urban energy system modeling and thermal building simulation based on OpenStreetMap data sets,
Building and Environment,
Volume 149,
Pages 630-639,
ISSN 0360-1323
[pdf](https://doi.org/10.1016/j.buildenv.2018.12.025),
[bibtex](https://github.com/RWTH-EBC/pyCity/tree/master/doc/S0360132318307686.bib)

If you require a reference in German language:
+ Schiefelbein, J. , Javadi, A. , Fuchs, M. , Müller, D. , Monti, A. and Diekerhof, M. (2017), Modellierung und Optimierung von Mischgebieten. Bauphysik, 39: 23-32. doi:10.1002/bapi.201710001
[pdf](https://doi.org/10.1002/bapi.201710001),
[bibtex](https://github.com/RWTH-EBC/pyCity/tree/master/doc/pericles_1437098039.bib)

## License

pyCity is released by RWTH Aachen University's E.ON Energy Research Center (E.ON ERC),
Institute for Energy Efficient Buildings and Indoor Climate (EBC) and
Institute for Automation of Complex Power Systems (ACS)
under the [MIT License](https://opensource.org/licenses/MIT)

## Acknowledgements

We gratefully acknowledge the financial support by BMWi 
(German Federal Ministry for Economic Affairs and Energy) 
under promotional references 03ET1138D and 03ET1381A.

<img src="https://www.innovation-beratung-foerderung.de/INNO/Redaktion/DE/Bilder/Titelbilder/titel_foerderlogo_bmwi.jpg?__blob=normal&v=3" width="200">
