"""
Last updated: 02Feb2020
              added documentation
              no longer builds shape_mini dictionary internally, but rather lets
              other scripts make that call
"""

import os
import sys


try:
    os.listdir('/usr')
    windows = False
    sys.path.append('/data/scripts/resources')
except:
    sys.path.append('C:/data/scripts/resources')

from reference_data import set_paths

data_dir,image_dir,archive_dir,gis_dir,placefile_dir = set_paths()


# please see documentation in resources/case_data.py for additional information


import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
#from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy.io.shapereader as shpreader

county_dir = 'counties'
state_dir = 'states'
interstate_dir = 'interstates'
places_dir = 'places'

# shapeDict categorizes each shapefile by type which also helps define the
# path to each shapefile


shapeDict = {}

# It's admittedly confusing, but a ST (state) key here refers to the counties for that state 
shapeDict['ND'] = {'type':county_dir,'shape_dir':'counties_nd','file':'counties_ND.shp'}
shapeDict['MN'] = {'type':county_dir,'shape_dir':'counties_mn','file':'counties_MN.shp'}
shapeDict['MI'] = {'type':county_dir,'shape_dir':'counties_mi','file':'counties_MI.shp'}
shapeDict['CO'] = {'type':county_dir,'shape_dir':'counties_co','file':'counties_CO.shp'}
shapeDict['KS'] = {'type':county_dir,'shape_dir':'counties_ks','file':'counties_KS.shp'}
shapeDict['MO'] = {'type':county_dir,'shape_dir':'counties_mo','file':'counties_MO.shp'}
shapeDict['OH'] = {'type':county_dir,'shape_dir':'counties_oh','file':'counties_OH.shp'}
shapeDict['IL'] = {'type':county_dir,'shape_dir':'counties_il','file':'counties_IL.shp'}
shapeDict['IN'] = {'type':county_dir,'shape_dir':'counties_in','file':'counties_IN.shp'}
shapeDict['IA'] = {'type':county_dir,'shape_dir':'counties_ia','file':'counties_IA.shp'}
shapeDict['WI'] = {'type':county_dir,'shape_dir':'counties_wi','file':'counties_WI.shp'}
shapeDict['SD'] = {'type':county_dir,'shape_dir':'counties_sd','file':'counties_SD.shp'}
shapeDict['WY'] = {'type':county_dir,'shape_dir':'counties_wy','file':'counties_WY.shp'}
shapeDict['WY'] = {'type':county_dir,'shape_dir':'counties_wy','file':'counties_WY.shp'}
shapeDict['states_CONUS'] = {'type':state_dir,'shape_dir':'states_CONUS','file':'states_CONUS.shp'}
shapeDict['interstates_conus'] = {'type':interstate_dir,'shape_dir':'interstates_conus','file':'interstates_conus.shp'}
shapeDict['NORTH_PLAINS_STATES'] = {'type':'states','shape_dir':'state_north_plains','file':'states_NORTH_PLAINS.shp'}
shapeDict['places_usa'] = {'type':places_dir,'shape_dir':'places_usa','file':'places_usa.shp'}

shapeDict['20180719_survey'] = {'type':'surveys','shape_dir':'survey_20180719','file':'extractDamagePolys.shp'}
shapeDict['20190314_survey'] = {'type':'surveys','shape_dir':'survey_20190314','file':'survey.shp'}
shapeDict['20190528_survey'] = {'type':'surveys','shape_dir':'survey_20190528','file':'20190528_survey.shp'}
shapeDict['20190720_paths'] = {'type':'surveys','shape_dir':'survey_20190720','file':'extractDamagePaths.shp'}
shapeDict['20190720_points'] = {'type':'surveys','shape_dir':'survey_20190720','file':'wind_damage_points.shp'}
shapeDict['20190704_survey'] = {'type':'surveys','shape_dir':'survey_20190704','file':'extractDamagePaths.shp'}
shapeDict['20190911_survey'] = {'type':'surveys','shape_dir':'survey_20190911','file':'manual_swath.shp'}
shapeDict['20080608_survey'] = {'type':'surveys','shape_dir':'survey_20080608','file':'lansing.shp'}
shapeDict['20220520_survey'] = {'type':'surveys','shape_dir':'survey_20220520','file':'nws_dat_damage_paths.shp'}
shapeDict['Lake_MI_counties'] = {'type':county_dir,'shape_dir':'Lake_MI_counties','file':'Lake_MI_counties.shp'}

shapelist = ['MI']

def get_shapefile(shape_path):
    reader = shpreader.Reader(shape_path)
    features = list(reader.geometries())
    SHAPEFILE = cfeature.ShapelyFeature(features, ccrs.PlateCarree())
    return SHAPEFILE


def make_shapes(shapelist):
    """
    This most flexible cartopy shapely creation method because it takes
    a user-defined list of desired shapefiles
    
    Parameters
    ----------
      shapelist :    list of strings
                     values of shapeDict keys associated with the shapefiles to be plotted
                   
    Dependencies
    ----------
   get_shapefile :   method
                     reads shapefile and creates Shape Feature


    Returns
    -------
       shape_mini :  dictionary of one or more items

                      key  --  string referring to shapefile
                    value  --  created cartopy Shapely Feature object
                            allows iterative cartopy plots using 
                            the cartopy add_feature method

    """             

    shape_mini = {}
    for t in shapelist:
        shape = shapeDict[t]
        shape_path = os.path.join(gis_dir,shape['type'],shape['shape_dir'],shape['file'])
        print(shape_path)
        SHAPE = get_shapefile(shape_path)
        shape_mini[t] = SHAPE
    return shape_mini




def make_MI_and_surrounding_state_counties():
    """
    It's common for me to want counties for Michigan and surrounding states
    So this is a hard-wired method for this using a pre-defined shapelist


    Returns
    -------
    shape_mini : a dictionary of cartopy Shapely Features ready to iteratively
                 called and plotted with the cartopy add_feature method
                 The "mini" refers to the fact this is likely a subset of options
                 in the shapeDict dictionary. The key difference being that
                 cartopy objects are actually created here 
                


    """
    shapelist = ['MI','WI','IN','IL', 'OH']
    shape_mini = {}
    for t in shapelist:
        shape = shapeDict[t]

        shape_path = os.path.join(gis_dir,shape['type'],shape['shape_dir'],shape['file'])
        print(shape_path)
        SHAPE = get_shapefile(shape_path)
        shape_mini[t] = SHAPE
    return shape_mini

def pyart_gis_layers():
    """
    This will be the standard list of layers to plot for pyart displays
    Typically, the pyart_plot.py script calls this with the following line:
        
        shape_mini = pyart_gis_layers()


    Dependencies
    ----------
    get_shapefile :   method
                     reads shapefile and creates Shape Feature

    Returns
    -------
    shape_mini : a dictionary of cartopy Shapely Features ready to iteratively
                 called and plotted with the cartopy add_feature method
                 The "mini" naming convention refers to fact this is likely a 
                 subset of options in the shapeDict dictionary.
                 The key difference being that cartopy objects are actually created here 
                


    """
    shapelist = ['interstates_conus','states_CONUS']
    shape_mini = {}
    for t in shapelist:
        shape = shapeDict[t]

        shape_path = os.path.join(gis_dir,shape['type'],shape['shape_dir'],shape['file'])
        print(shape_path)
        SHAPE = get_shapefile(shape_path)
        shape_mini[t] = SHAPE
        
    return shape_mini



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

