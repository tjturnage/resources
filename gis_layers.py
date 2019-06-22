# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 08:16:00 2019

@author: tjtur
"""

def get_shapefile(shape_path):
    reader = shpreader.Reader(shape_path)
    features = list(reader.geometries())
    SHAPEFILE = cfeature.ShapelyFeature(features, ccrs.PlateCarree())
    return SHAPEFILE


import os
from case_data import this_case
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
#from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy.io.shapereader as shpreader


try:
    os.listdir('/var/www')
    base_gis_dir = '/data/GIS'
except:
    base_gis_dir = 'C:/data/GIS'




shapeDict = {}
#shapeDict['ND'] = {'shape_dir':'counties_nd','file':'counties_ND.shp','shape_name':'COUNTIES_ND'}
#shapeDict['MN'] = {'shape_dir':'counties_mn','file':'counties_MN.shp','shape_name':'COUNTIES_MN'}
#shapeDict['MI'] = {'shape_dir':'counties_mi','file':'counties_MI.shp','shape_name':'COUNTIES_MI'}
shapeDict['ND'] = {'shape_dir':'counties_nd','file':'counties_ND.shp'}
shapeDict['MN'] = {'shape_dir':'counties_mn','file':'counties_MN.shp'}
shapeDict['MI'] = {'shape_dir':'counties_mi','file':'counties_MI.shp'}
shapeDict['CO'] = {'shape_dir':'counties_co','file':'counties_CO.shp'}
shapeDict['KS'] = {'shape_dir':'counties_ks','file':'counties_KS.shp'}
shapeDict['MO'] = {'shape_dir':'counties_mo','file':'counties_MO.shp'}


shapelist = this_case['shapelist']
#shapelist = ['KS','CO','MO']
shape_mini = {}
for t in shapelist:
    shape = shapeDict[t]
    shape_file = shape['file']
    shape_path = os.path.join(base_gis_dir,shape['shape_dir'],shape['file'])
    SHAPE = get_shapefile(shape_path)
    shape_mini[t] = SHAPE



states = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_1_states_provinces_lines',
        scale='50m',
        facecolor='none')

lon_formatter = LongitudeFormatter(number_format='.1f',
                       degree_symbol='',
                       dateline_direction_label=False,
                       zero_direction_label=True)

lat_formatter = LatitudeFormatter(number_format='.1f',
                      degree_symbol='')

