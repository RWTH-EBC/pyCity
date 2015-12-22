"""
Script to generate city district (building objects with demand and position; Without energy systems)
This script assumes buildings with single zoning.
"""

from __future__ import division
import os
import math
import pandas
import pickle

import sympy.geometry.point as point

import pycity.classes.Timer
import pycity.classes.Weather
import pycity.classes.Prices
import pycity.classes.Environment

import pycity.classes.demand.Apartment as Apartment
import pycity.classes.demand.DomesticHotWater as DomesticHotWater
import pycity.classes.demand.ElectricalDemand as ElectricalDemand
import pycity.classes.demand.SpaceHeating as SpaceHeating
import pycity.classes.HeatingCurve as HeatingCurve
import pycity.classes.Building as Building
import pycity.classes.CityDistrict as citydis
import pycity.classes.demand.Occupancy as occu


def run_city_generator(gen_mo=0, input_name='test_city_only_buildings.txt', output_name=None, use_el_slp=True,
                       gen_dhw_profile=False):
    """
    Function to generate and return city district object

    Parameters
    ----------
    gen_mo : int, optional
        Generation mode number:
        0 - Use data from input file (default)
    input_name : str, optional
        Name of input data file (default: 'test_city_only_buildings.txt')
    output_name : str, optional
        Name of output file (default: None)
        If output_name is None, no output file is generated. Else: Pickled output file is saved to output folder
    use_el_slp : bool, optional
        Boolean to define, how electrical load profile should be generated (default: True)
        True: Generate el. load profile via el. slp
        False: Use stochastic profile generator (only valid for residential buildings!)
    gen_dhw_profile : bool, optional
        Boolean to define, if domestic hot water profile should be generated (default: False)
        True: Generate dhw profile (valid for residential buildings!)
        False: Do not generate dhw profile

    Returns
    -------
    city_district : object
        CityDistrict object of PyCity
    """

    #  Generate timer, weather and price objects
    timer = pycity.classes.Timer.Timer()
    weather = pycity.classes.Weather.Weather(timer)
    prices = pycity.classes.Prices.Prices()

    #  Generate environment
    environment = pycity.classes.Environment.Environment(timer, weather, prices)

    #  Generate city district object
    city_district = citydis.CityDistrict(environment)

    #  Current file path
    curr_path = os.path.dirname(os.path.abspath(__file__))

    #  Choose city district generation method
    if gen_mo == 0:  # Load data from file
        import_path = os.path.join(curr_path, 'input', input_name)
        city_dist_pandas_dataframe = pandas.read_csv(import_path, sep='\t')

        for index, row in city_dist_pandas_dataframe.iterrows():
            curr_name = row['name']  # Building name
            curr_x = row['x_coord / m']  # Building x coordinate in m
            curr_y = row['y_coord / m']  # Building y coordinate in m
            curr_area = row['living_area / m2']  # Net floor area (respectively living area) in m2
            curr_th_spec_demand = row['specific_th_demand / kWh/m2a']  # Spec. thermal energy demand in kWh/m2a
            curr_el_demand = row['an_el_demand / kWh/a']  # Annual electric energy demand in kWh/a
            curr_th_slp = row['th_slp_profile_type']  # Thermal SLP type
            curr_el_slp = row['el_slp_profile_type']  # Electrical SLP type
            curr_total_nb_occupants = row['total_nb_occupants']  # Total number of occupants in building

            #  Assert input values
            assert curr_area > 0
            assert curr_th_spec_demand > 0
            assert curr_el_demand > 0

            print('Processing building', curr_name)

            #  Check if number of occupants is nan (for non residential buildings)
            if math.isnan(curr_total_nb_occupants):
                curr_total_nb_occupants = None  # Replace nan with None
            else:  # If number of occupants is not nan, convert value to integer
                curr_total_nb_occupants = int(curr_total_nb_occupants)
                assert curr_total_nb_occupants >= 1
                assert curr_total_nb_occupants <= 5

            #  Generate heat demand curve for space heating
            heat_demand = SpaceHeating.SpaceHeating(environment,
                                                    method=1,  # Standard load profile
                                                    livingArea=curr_area,
                                                    specificDemand=curr_th_spec_demand,
                                                    profile_type=curr_th_slp)

            if use_el_slp:  # Use el. SLP
                el_method = 1
                occupancy_profile = []  # Dummy value
            else:  # Stochastic profile generator (only for residential buildings)
                el_method = 2
                #  Generate stochastic occupancy profile
                occupancy_object = occu.Occupancy(environment, number_occupants=curr_total_nb_occupants)
                occupancy_profile = occupancy_object.occupancy

            #  Generate electrical demand curve
            el_demand = ElectricalDemand.ElectricalDemand(environment,
                                                          method=el_method,
                                                          annualDemand=curr_el_demand, profileType=curr_el_slp,
                                                          singleFamilyHouse=True,
                                                          total_nb_occupants=curr_total_nb_occupants,
                                                          randomizeAppliances=True, lightConfiguration=0,
                                                          occupancy=occupancy_profile)

            #  Generate apartment and add demand durves
            apartment = Apartment.Apartment(environment)
            apartment.addMultipleEntities([heat_demand, el_demand])

            if gen_dhw_profile:
                #  Generate domestic hot water demand curve
                dhw_annex42 = DomesticHotWater.DomesticHotWater(environment,
                                                                tFlow=60,
                                                                thermal=True,
                                                                method=1,  # Annex 42
                                                                dailyConsumption=70,
                                                                supplyTemperature=25)
                apartment.addEntity(dhw_annex42)

            #  Generate heating curve
            heatingCurve = HeatingCurve.HeatingCurve(environment)

            #  Generate building and add apartment and heating curve
            building = Building.Building(environment)
            entities = [apartment, heatingCurve]
            building.addMultipleEntities(entities)

            #  Generate sympy point positions
            position = point.Point(curr_x, curr_y)

            #  Add buildings to city district
            city_district.addEntity(entity=building, position=position, name=curr_name)

            print('Added building', curr_name, ' to city district.')

    #  Save results as pickled file
    if output_name is not None:
        output_path = os.path.join(curr_path, 'output', output_name)
        #  Pickle and dump city objects
        pickle.dump(city_district, open(output_path, 'wb'))
        print('Pickled and dumped city object')

    return city_district

if __name__ == '__main__':

    #  User inputs  #########################################################################

    #  Choose generation mode
    #  0 - Use csv/txt input to generate city district
    generation_mode = 0

    #  Choose if electrical load profiles should be generated via slp or via stochastic profile generator
    #  Stochastic profiles are only valid for residential buildings!
    use_el_slp = True

    #  Choose if dhw profile should be generated (only valid for residential buildings)
    gen_dhw_profile = True

    #  Define input data filename
    #  filename = 'test_city_only_residential_buildings.txt'
    filename = 'test_city_mixed_buildings.txt'

    #  Define ouput data filename (pickled city object)
    #  pickle_city_filename = 'myCity.p'
    pickle_city_filename = None

    #  Run city district generator
    city_district = run_city_generator(gen_mo=generation_mode, input_name=filename, output_name=pickle_city_filename,
                       use_el_slp=use_el_slp, gen_dhw_profile=gen_dhw_profile)

    print('What am I?')
    print(city_district)
    print('\n')

    print('Nodes of city district with data:')
    print(city_district.nodes(data=True))
    print('\n')

    demand_tuple = city_district.node[1001]['entity'].getDemands()
    print('Building 1001 thermal energy demand:')
    print(demand_tuple[0])
    print('Building 1001 electrical energy demand:')
    print(demand_tuple[1])
    print('\n')

