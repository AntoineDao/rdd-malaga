import uwg
from dragonfly.terrain import Terrain
from dragonfly.vegetation import Vegetation
from dragonfly.typology import Typology
from dragonfly.dfparameter import BoundaryLayerPar, PavementPar, RefEPWSitePar,\
    TrafficPar, VegetationPar
from dragonfly.city import City
from ladybug.analysisperiod import AnalysisPeriod
from utils import create_uwg, set_uwg_input, set_individual_typologies,\
    set_global_facade_props

import os
import json

# File management
epw_file = os.path.abspath('ESP_Malaga.084820_SWEC.epw')
folder = 'uwg_epws'
name = '0_baseline.epw'

# Analysis Period
analysis_period = AnalysisPeriod(st_month=1, st_day=1, st_hour=0,
                                 end_month=12, end_day=31, end_hour=23,
                                 timestep=1, is_leap_year=False)


# Parameters setup
tp_dict = {
    'sensible_heat': 4,
    'weekday_schedule': [],
    'saturday_schedule': [],
    'sunday_schedule': []
}

vg_dict = {
    'vegetation_albedo': 0.25,
    'vegetation_start_month': 4,
    'vegetation_end_month': 11,
    'tree_latent_fraction': 0.7,
    'grass_latent_fraction': 0.5,
}

traffic_parameters = TrafficPar(sensible_heat=tp_dict['sensible_heat'])

vegetation_parameters = VegetationPar(vegetation_start_month=vg_dict['vegetation_start_month'],
                                      vegetation_end_month=vg_dict['vegetation_end_month'])

pavement_parameters = PavementPar() # will use defaults because i don't know any better

ref_epw_site_par = RefEPWSitePar(average_obstacle_height=None,
                                 vegetation_coverage=0.7,
                                 temp_measure_height=None,
                                 wind_measure_height=None)

boundary_layer_par = BoundaryLayerPar()

# Climate zone
climate_zone = '3A'

# Terrain setup
terrain_area = 160000
# terrain_char_len = 300

terrain = Terrain(area=terrain_area)

# Vegetation setup
tree_area = 20
grass_area = 30

trees = Vegetation(area=tree_area, is_trees=True)
grass = Vegetation(area=grass_area, is_trees=False)


# Typologies setup
# Need to setup residential, office, cafes and retail

resi_dict = {
    'average_height': 24,
    'footprint_area': 52000,
    'facade_area': 221000,
    'bldg_program': 'MidRiseApartment',
    'bldg_age': 'Pre1980s',
    'fract_heat_to_canyon': 0.7,
    'glz_ratio': 0.3,
    'floor_area': 391000
}

residential = Typology(average_height=resi_dict['average_height'],
                       footprint_area=resi_dict['footprint_area'],
                       facade_area=resi_dict['facade_area'],
                       bldg_program=resi_dict['bldg_program'],
                       bldg_age=resi_dict['bldg_age'],
                       fract_heat_to_canyon=resi_dict['fract_heat_to_canyon'],
                       glz_ratio=resi_dict['glz_ratio'],
                       floor_area=resi_dict['floor_area'])

# residential.wall_albedo =
# residential.roof_albedo =
residential.roof_veg_fraction = 0.5

sm_retail = {
    'average_height': 8,
    'footprint_area': 2256,
    'facade_area': 2424,
    'bldg_program': 'StandAloneRetail',
    'bldg_age': 'Pre1980s',
    'fract_heat_to_canyon': 0.7,
    'glz_ratio': 0.3,
    'floor_area': 4511
}

small_retail = Typology(average_height=sm_retail['average_height'],
                        footprint_area=sm_retail['footprint_area'],
                        facade_area=sm_retail['facade_area'],
                        bldg_program=sm_retail['bldg_program'],
                        bldg_age=sm_retail['bldg_age'],
                        fract_heat_to_canyon=sm_retail['fract_heat_to_canyon'],
                        glz_ratio=sm_retail['glz_ratio'],
                        floor_area=sm_retail['floor_area'])


small_office_dict = {
    'average_height': 18,
    'footprint_area': 300,
    'facade_area': 200,
    'bldg_program': 'SmallOffice',
    'bldg_age': 'NewConstruction',
    'fract_heat_to_canyon': 0.7,
    'glz_ratio': 0.3
}

small_office = Typology(average_height=small_office_dict['average_height'],
                        footprint_area=small_office_dict['footprint_area'],
                        facade_area=small_office_dict['facade_area'],
                        bldg_program=small_office_dict['bldg_program'],
                        bldg_age=small_office_dict['bldg_age'],
                        fract_heat_to_canyon=small_office_dict['fract_heat_to_canyon'],
                        glz_ratio=small_office_dict['glz_ratio'])

# small_office.wall_albedo =
# small_office.roof_albedo =
small_office.roof_veg_fraction = 0.5

cafes_dict = {
    'average_height': 18,
    'footprint_area': 300,
    'facade_area': 200,
    'bldg_program': 'QuickServiceRestaurant',
    'bldg_age': '1980sPresent',
    'fract_heat_to_canyon': 0.7,
    'glz_ratio': 0.3
}

cafes = Typology(average_height=cafes_dict['average_height'],
                 footprint_area=cafes_dict['footprint_area'],
                 facade_area=cafes_dict['facade_area'],
                 bldg_program=cafes_dict['bldg_program'],
                 bldg_age=cafes_dict['bldg_age'],
                 fract_heat_to_canyon=cafes_dict['fract_heat_to_canyon'],
                 glz_ratio=cafes_dict['glz_ratio'])

# typologies = [residential, small_retail, supermarket, small_office, cafes]
typologies = [residential]

# And now for the city!

city = City.from_typologies(typologies=typologies, terrain=terrain,
                            climate_zone=climate_zone,
                            traffic_parameters=traffic_parameters,
                            tree_coverage_ratio=0,
                            grass_coverage_ratio=0,
                            vegetation_parameters=vegetation_parameters,
                            pavement_parameters=pavement_parameters)


"""
ABOVE THIS IS PREP

BLOW THIS IS SIMULATION RUN
"""
# create a uwg_object from the dragonfly objects.
uwg_object, new_epw_path = create_uwg(epw_file, folder, name)
uwg_object = set_uwg_input(uwg_object, city, ref_epw_site_par,
                           boundary_layer_par, analysis_period)

"""
This is a HACK! Need to set DOE filepath as default in uwg...
"""

uwg_object.init_BEM_obj()
# uwg_object = set_uwg_input(uwg_object, city, ref_epw_site_par, boundary_layer_par, analysis_period)
uwg_object = set_individual_typologies(uwg_object, city)
uwg_object = set_global_facade_props(uwg_object, city)

# get the object ready to simulate
uwg_object.read_epw()


uwg_object.init_input_obj()
uwg_object.hvac_autosize()

uwg_object.simulate()
uwg_object.write_epw()
