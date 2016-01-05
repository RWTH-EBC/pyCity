import pytest

import pycity.classes.Timer
import pycity.classes.Weather
import pycity.classes.Environment
import pycity.classes.Prices

import pycity.classes.demand.DomesticHotWater as DomesticHotWater
import pycity.classes.demand.ElectricalDemand as ElectricalDemand
import pycity.classes.demand.SpaceHeating as SpaceHeating


@pytest.fixture(scope='module')
def create_environment():
    """
    Fixture to create environment object for PyCity (scope='module')

    Returns
    -------
    create_environment : environment object
    """
    timer = pycity.classes.Timer.Timer(timeDiscretization=900,
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
