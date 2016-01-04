import pytest

import pycity.classes.Timer
import pycity.classes.Weather
import pycity.classes.Environment
import pycity.classes.Prices


@pytest.fixture
def create_environment():
    timer = pycity.classes.Timer.Timer(timeDiscretization=900,
                                       timestepsTotal=365*24*4,
                                       initialDay=1)
    weather = pycity.classes.Weather.Weather(timer, useTRY=True)
    prices = pycity.classes.Prices.Prices()

    create_environment = pycity.classes.Environment.Environment(timer, weather,
                                                         prices)
    return create_environment
