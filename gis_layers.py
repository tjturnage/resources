# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 08:16:00 2019

@author: tjtur
"""

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
shapeDict['ND'] = {'type':'county','shape_dir':'counties_nd','file':'counties_ND.shp'}
shapeDict['MN'] = {'type':'county','shape_dir':'counties_mn','file':'counties_MN.shp'}
shapeDict['MI'] = {'type':'county','shape_dir':'counties_mi','file':'counties_MI.shp'}
shapeDict['CO'] = {'type':'county','shape_dir':'counties_co','file':'counties_CO.shp'}
shapeDict['KS'] = {'type':'county','shape_dir':'counties_ks','file':'counties_KS.shp'}
shapeDict['MO'] = {'type':'county','shape_dir':'counties_mo','file':'counties_MO.shp'}
shapeDict['OH'] = {'type':'county','shape_dir':'counties_oh','file':'counties_OH.shp'}
shapeDict['IL'] = {'type':'county','shape_dir':'counties_il','file':'counties_IL.shp'}
shapeDict['IN'] = {'type':'county','shape_dir':'counties_in','file':'counties_IN.shp'}
shapeDict['WI'] = {'type':'county','shape_dir':'counties_wi','file':'counties_WI.shp'}
shapeDict['SD'] = {'type':'county','shape_dir':'counties_sd','file':'counties_SD.shp'}
shapeDict['WY'] = {'type':'county','shape_dir':'counties_wy','file':'counties_WY.shp'}
shapeDict['Lake_MI_counties'] = {'type':'county','shape_dir':'Lake_MI_counties','file':'Lake_MI_counties.shp'}
shapeDict['20190314_survey'] = {'type':'survey','shape_dir':'survey_20190314','file':'survey.shp'}
shapeDict['20190528_survey'] = {'type':'survey','shape_dir':'survey_20190528','file':'20190528_survey.shp'}
shapeDict['20190720_paths'] = {'type':'survey','shape_dir':'survey_20190720','file':'extractDamagePaths.shp'}
shapeDict['20190720_points'] = {'type':'survey','shape_dir':'survey_20190720','file':'wind_damage_points.shp'}
shapeDict['20190704_survey'] = {'type':'survey','shape_dir':'survey_20190704','file':'extractDamagePaths.shp'}
shapeDict['20190911_survey'] = {'type':'survey','shape_dir':'survey_20190911','file':'manual_swath.shp'}
shapelist = this_case['shapelist']
#shapelist = ['KS','CO','MO']

def get_shapefile(shape_path):
    reader = shpreader.Reader(shape_path)
    features = list(reader.geometries())
    SHAPEFILE = cfeature.ShapelyFeature(features, ccrs.PlateCarree())
    return SHAPEFILE


def make_shapes():
    shape_mini = {}
    for t in shapelist:
        shape = shapeDict[t]
        shape_type = shape['type']
        if shape_type == 'county':
            shape_path = os.path.join(base_gis_dir,'counties',shape['shape_dir'],shape['file'])
        elif shape_type == 'survey':
            shape_path = os.path.join(base_gis_dir,'surveys',shape['shape_dir'],shape['file'])
        else:
            pass
        print(shape_path)
        SHAPE = get_shapefile(shape_path)
        shape_mini[t] = SHAPE
    return shape_mini

def make_shapes_mi():
    shape_michigan = {}
    shape = shapeDict['MI']
    shape_path = os.path.join(base_gis_dir,'counties',shape['shape_dir'],shape['file'])
    print(shape_path)
    SHAPE = get_shapefile(shape_path)
    shape_michigan['MI'] = SHAPE
    return shape_michigan


def make_states():
    shapelist = ['MI','WI','IN','IL']
    shape_mini = {}
    for t in shapelist:
        shape = shapeDict[t]
        shape_type = shape['type']
        if shape_type == 'county':
            shape_path = os.path.join(base_gis_dir,'counties',shape['shape_dir'],shape['file'])
        elif shape_type == 'survey':
            shape_path = os.path.join(base_gis_dir,'surveys',shape['shape_dir'],shape['file'])
        else:
            pass
        print(shape_path)
        SHAPE = get_shapefile(shape_path)
        shape_mini[t] = SHAPE
    return shape_mini

shape_states = make_states()
shape_michigan = make_shapes_mi()
shape_mini = make_shapes()

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

