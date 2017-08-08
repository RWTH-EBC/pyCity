# coding=utf-8

import pytest
import shapely.geometry.point as point

import pycity.classes.Timer
import pycity.classes.Weather
import pycity.classes.Environment
import pycity.classes.Prices

import pycity.classes.demand.DomesticHotWater as DomesticHotWater
import pycity.classes.demand.ElectricalDemand as ElectricalDemand
import pycity.classes.demand.SpaceHeating as SpaceHeating
import pycity.classes.demand.Occupancy as Occupanc
import pycity.classes.demand.Apartment as App
import pycity.classes.Building as Build
import pycity.classes.CityDistrict as citydist


@pytest.fixture(scope='module')
def create_environment(timestep=900):
    """
    Fixture to create environment object for PyCity (scope='module')

    Parameters
    ----------
    timestep : int, optional
        Integer timestep in seconds (default: 900)

    Returns
    -------
    create_environment : environment object
    """
    timer = pycity.classes.Timer.Timer(timeDiscretization=timestep,
                                       timestepsTotal=365 * 24 * 4,
                                       initialDay=1)
    weather = pycity.classes.Weather.Weather(timer, useTRY=True)
    prices = pycity.classes.Prices.Prices()

    create_environment = pycity.classes.Environment.Environment(timer, weather,
                                                                prices)
    return create_environment


@pytest.fixture
def create_demands(create_environment):
    """
    Fixture to create space heating, dhw and electrical demands
    (for residential buildings; with standardized load profiles (SLP))

    Parameters
    ----------
    create_environment : object
        Environment object (as fixture of pytest)

    Returns
    -------
    create_demands : tuple (of np.arrays)
        Tuple with demand arrays (heat_demand, el_demand, dhw_demand)
    """
    #  Generate heating demand
    heat_demand = SpaceHeating.SpaceHeating(create_environment,
                                            method=1,  # Standard load profile
                                            livingArea=100,
                                            specificDemand=150)

    el_demand = ElectricalDemand.ElectricalDemand(create_environment,
                                                  method=1,
                                                  # Standard load profile
                                                  annualDemand=3000)

    daily_consumption = 70
    t_flow = 70
    supply_temp = 25
    dhw_annex42 = DomesticHotWater.DomesticHotWater(create_environment,
                                                    tFlow=t_flow,
                                                    thermal=True,
                                                    method=1,  # Annex 42
                                                    dailyConsumption=daily_consumption,
                                                    supplyTemperature=supply_temp)

    create_demands = (heat_demand, el_demand, dhw_annex42)

    return create_demands


@pytest.fixture
def create_occupancy(create_environment, nb_occupants=1):
    """
    Pytest fixture function to generate occupancy object.

    Parameters
    ----------
    create_environment : object
        Environment object (as fixture of pytest)
    nb_occupants : int, optional
        Number of occupants (default: 1)

    Returns
    -------
    create_occupancy : object
        occupancy object
    """
    create_occupancy = \
        pycity.classes.demand.Occupancy.Occupancy(create_environment,
                                                  number_occupants=nb_occupants)

    return create_occupancy


@pytest.fixture
def create_empty_citydist(create_environment):
    """
    Pytest fixture function to generate city district

    Parameters
    ----------
    create_environment : object
        Environment object (as fixture of pytest)

    Returns
    -------
    create_empty_citydist : object
        CityDistrict object of PyCity
    """
    create_empty_citydist = citydist.CityDistrict()

    #  Add environment
    create_empty_citydist.environment = create_environment

    return create_empty_citydist


@pytest.fixture
def create_citydist(create_environment, create_building):
    """
    Pytest fixture function to generate city district with three
    res. buildings (with demands) on positions (0, 0), (0, 10), (10, 10)

    Parameters
    ----------
    create_environment : object
        Environment object (as fixture of pytest)

    Returns
    -------
    create_citydistrict : object
        CityDistrict object of PyCity
    """
    create_citydist = citydist.CityDistrict()

    #  Add environment
    create_empty_citydist.environment = create_environment

    create_citydist.addEntity(entity=create_building,
                              position=point.Point(0, 0))
    create_citydist.addEntity(entity=create_building,
                              position=point.Point(0, 10))
    create_citydist.addEntity(entity=create_building,
                              position=point.Point(10, 10))

    return create_citydist


@pytest.fixture
def create_apartment(create_environment, create_demands):
    """
    Pytest fixture function to generate apartment object (with demands)

    Parameters
    ----------
    create_environment : object
        Environment object (as fixture of pytest)
    create_demands : tuple (of np.arrays)
        Tuple with demand arrays (heat_demand, el_demand, dhw_demand)

    Returns
    -------
    create_apartment : object
        Apartment object
    """
    create_apartment = App.Apartment(environment=create_environment)
    create_apartment.addMultipleEntities(create_demands)
    return create_apartment


@pytest.fixture
def create_building(create_environment, create_apartment):
    """
    Pytest fixture function to generate building object (with demands,
    without BES or heating-curve)

    Parameters
    ----------
    create_environment : object
        Environment object (as fixture of pytest)
    create_apartment : object
        Apartment object (with demands)

    Returns
    -------
    create_building : object
        Building object
    """
    create_building = Build.Building(environment=create_environment)
    create_building.addEntity(entity=create_apartment)
    return create_building
