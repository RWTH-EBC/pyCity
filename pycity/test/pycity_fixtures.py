import pytest

import pycity.classes.Timer
import pycity.classes.Weather
import pycity.classes.Environment
import pycity.classes.Prices

import pycity.classes.demand.DomesticHotWater as DomesticHotWater
import pycity.classes.demand.ElectricalDemand as ElectricalDemand
import pycity.classes.demand.SpaceHeating as SpaceHeating
import pycity.classes.demand.Occupancy as Occupanc


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
                                       timestepsTotal=365*24*4,
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
                                            method=1, # Standard load profile
                                            livingArea=100,
                                            specificDemand=150)

    el_demand = ElectricalDemand.ElectricalDemand(create_environment,
                                          method=1, # Standard load profile
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
    occupancy_object = \
        pycity.classes.demand.Occupancy.Occupancy(create_environment,
                                                  number_occupants=nb_occupants)

    create_occupancy = occupancy_object.occupancy

    return create_occupancy
