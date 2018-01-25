import pygal_maps_world.maps
import json
from pygal.style import RotateStyle

from country_codes import get_country_code

filename = 'C:/Users/linji/Desktop/HW/python/DataVisualization/JSON/gdp_json.json'
with open(filename) as f:
    gdp_data = json.load(f)

cc_gdps = {}
for gdp_dict in gdp_data:
    if gdp_dict['Year'] == 2016:
        country_name = gdp_dict['Country Name']
        gdp = float(gdp_dict['Value'])
        code = get_country_code(country_name)
        if code:
            cc_gdps[code] = gdp
cc_gdps_1, cc_gdps_2, cc_gdps_3 = {}, {}, {}
for cc, gdp in cc_gdps.items():
    if gdp < 10000000000:
        cc_gdps_1[cc] = gdp
    elif gdp < 1000000000000:
        cc_gdps_2[cc] = gdp
    else:
        cc_gdps_3[cc] = gdp
wm_style = RotateStyle('#996633')
wm = pygal_maps_world.maps.World(style=wm_style)
wm.title = 'GDP By Country 2016'
wm.add('<e+10', cc_gdps_1)
wm.add('<e+12', cc_gdps_2)
wm.add('>e+12', cc_gdps_3)
wm.render_to_file('C:/Users/linji/Desktop/HW/python/DataVisualization/JSON/world_gdp.svg')
