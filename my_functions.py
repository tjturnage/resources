# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 09:33:56 2019
Updated: 10/21/19

added the following for dynamic creation of figure sizes:
- define_mosaic_size

added the following for satellite-create-figures:
- add_radar_paths
- make_radar_array
- ltg_plot

"""

import os
import re
import shutil
import math
import pathlib
from datetime import datetime,timezone,timedelta
import pandas as pd
import matplotlib as plt
import numpy as np
from pyproj import Geod
from operator import itemgetter
from itertools import groupby
import xarray as xr


def wind_chill(t,s):
    """
    Returns wind chill in degress F
    Inputs:
        t   : temperatures in degrees F
        s   : wspd in MPH
    """    
    wc = 35.74 + 0.6215*t - 35.75*(s**0.16) + 0.4275*t*(s**0.16)
    #print(round(wc))
    return round(wc)

def time_to_frostbite(wc,s):
    if wc >= -15:
        fbt = 4
    if wc < -15:
        fbt = 3
    if wc < -35:
        if s > 20:
            fbt = 2
        else:
            fbt = 3
    if wc < -45:
        if s > 10:
            fbt = 2
        else:
            fbt = 3
                
    return fbt

def define_mosaic_size(products):
    mosaic_size = {}
    mosaic_size[2] = {'h':6,'w':15,'rows':1,'columns':2}
    mosaic_size[3] = {'h':6,'w':17,'rows':1,'columns':3}
    mosaic_size[4] = {'h':12,'w':14,'rows':2,'columns':2}
    mosaic_size[6] = {'h':12,'w':20,'rows':2,'columns':3}
    height = mosaic_size[len(products)]['h']
    width = mosaic_size[len(products)]['w']
    rows = mosaic_size[len(products)]['rows']
    cols = mosaic_size[len(products)]['columns']
    return width, height, rows, cols



def categorize(data_list,element):
    """dat
 [0,1,2,3,4,5,6],'major_yticks_labels':['0.00','0.01','0.05','0.10','0.2','0.3','0.5'], 
        zr_list   : one hourly snow in hundredths
    
    """

    vis_dict = {'0.0':0,'0.3':1,'0.6':2,'1':3,'2':4,'4':3,'6':6}
    zr_dict = {'-0.1':0,'1':1,'8':2,'18':3,'28':4,'45':5}
    sn_dict = {'-0.1':0,'0.05':1,'0.15':2,'0.45':3,'0.75':4,'0.95':5,'1.35':6,'1.85':7}  
    wc_dict = {'-20':6,'-10':5,'0':4,'10':3,'20':2,'30':1,}
    #sn_dict = {'-0.1':0,'0.05':1,'0.15':2,'0.33':3,'0.75':4,'1.5':5,'2.5':6}    

    if element == 'sn':
        data_dict = sn_dict
    if element == 'zr':
        data_dict = zr_dict    
    if element == 'vis':
        data_dict = vis_dict    
    if element == 'wc':
        data_dict = wc_dict


    category_list = []  
    for x in range(0,len(data_list)):
        val = data_list[x]
        for key in data_dict:
            if val > float(key):
                x_cat = data_dict[key]
            
        category_list.append(x_cat)

    return category_list

def dtList_nbm(run_dt,bulletin_type,tz_shift):
    """
      Create pandas date range of forecast valid times based on bulletin
      issuance time and bulletin type.
    
      Parameters
      ----------
        run_dt : python datetime object
                 Contains yr,mon,date,hour associated with bulletin issue time

  bulletin_type: string

                 'nbhtx' -- hourly guidance ( hourly)

                 This is required to define model forecast hour start and 
                 end times as a well as forecast hour interval.
                  
      Returns
      -------
           pandas date/time range to be used as index as well as start/end times
    """

    fcst_hour_zero_utc = run_dt + timedelta(hours=0)
    fcst_hour_zero_local = fcst_hour_zero_utc - timedelta(hours=tz_shift)
    #pTime = pd.Timestamp(fcst_hour_zero_utc)
    pTime = pd.Timestamp(fcst_hour_zero_local)
    idx = pd.date_range(pTime, periods=27, freq='H')

    return idx, fcst_hour_zero_local


def create_process_file_list(src_dir,product_list,cut_list,windows):
    part_list = []
    #Builds a sorted list of full file paths
    file_list = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(src_dir)) for f in fn]

    for f in file_list:
        p = pathlib.PurePath(f)
        parts = p.parts
        part_list.append(parts)
    
    sorted_path_list = []

    part_list.sort(key=itemgetter(-1))
    y = groupby(part_list,itemgetter(-2))        
    for y in part_list:
        z = list(y)
        this_one = "/".join(str(x) for x in z)
        if windows:
            this_one = this_one[0:2] + this_one[3:]

        sorted_path_list.append(this_one)

    trimmed_path_list = []
    for path in range(0,len(sorted_path_list)):
        src_filepath = str(sorted_path_list[path])
        #for product in product_list:

        for cuts in cut_list:
            if cuts in src_filepath:
                for product in product_list:
                    if product in src_filepath and 'Gradient' not in src_filepath and 'Aliased' not in src_filepath:
                        trimmed_path_list.append(sorted_path_list[path])
                        #print(str(sorted_path_list[path]))
    
    return trimmed_path_list

def add_radar_paths(file_dir,separator,code,met_info):
    """
    Build list of file paths to use for radar data
    This is commonly called from 'sat-the-final-chapter' with creating radar/satellite mosaic combos
    
    Parameters
    ----------
    file_dir : string
               The directory containing the netcdf files from which a subset
               gets selected.
   separator : string
               string to use for splitting - typically '.'
        code : string
               use 'r' for reflectivity
               use 'v' for velocity
    met_info : array
               a collection of absolute filepaths to the data sources for plotting
                   
    Returns
    -------
         Nothing, just appends to met list
    """
    files = os.listdir(file_dir)
    for z in files:
        file_info = str.split(z,'.')
        file_time_str = file_info[0]
        file_datetime = datetime.strptime(file_time_str,"%Y%m%d-%H%M%S")
        info = [file_datetime,code,os.path.join(file_dir,z)]
        met_info.append(info)
    return

def latlon_from_radar(data):
    """
    Convert radar bin radial coordinates to lat/lon coordinates.
    Adapted from Brian Blaylock code
    
    Parameters
    ----------
          az : numpy array
               All the radials for that particular product and elevation
               Changes from 720 radials for super-res product cuts to 360 radials
   elevation : float
               The radar elevation slice in degrees. Needed to calculate range 
               gate length (gate_len) as projected on the ground using simple
               trigonometry. This is a very crude approximation that doesn't
               factor for terrain, earth's curvature, or standard beam refraction.
   num_gates : integer
               The number of gates in a radial, which varies with 
               elevation and radar product. That is why each product makes 
               an individual call to this function. 
   radar_lat : float
               The latitude of the radar locations in decimal degrees
   radar_lon : float
               The longitude of the radar locations in decimal degrees
                   
    Returns
    -------
         lat : array like
         lon : array like
        back : I have no idea what this is for. I don't use it.
                    
    """
    dnew2 = data.sortby('Azimuth')
    azimuths = dnew2.Azimuth.values
    radar_lat = dnew2.Latitude
    radar_lon = dnew2.Longitude
    elevation = data.Elevation
    num_gates = len(dnew2.Gate)
    rng = None
    factor = math.cos(math.radians(elevation))
    if num_gates <= 334:
        gate_len = 1000.0 * factor
    else:
        gate_len = 250.0 * factor
    rng = np.arange(2125.0,(num_gates*gate_len + 2125.0),gate_len)
    g = Geod(ellps='clrk66')
    center_lat = np.ones([len(azimuths),len(rng)])*radar_lat
    center_lon = np.ones([len(azimuths),len(rng)])*radar_lon
    az2D = np.ones_like(center_lat)*azimuths[:,None]
    rng2D = np.ones_like(center_lat)*np.transpose(rng[:,None])
    lat,lon,back=g.fwd(center_lon,center_lat,az2D,rng2D)
    return dnew2,lat,lon,back

def make_radar_array(ds,ds_type):
    """
    This is a condensed version of radar data mapping used with satellite
    plotting in satellite-create-figures. The assumption is that we're
    only interested in reflectivity or velocity
    """
    data = xr.open_dataset(ds)
    dnew2,lats,lons,back=latlon_from_radar(data)
    if ds_type == 'Ref':
        da = dnew2.ReflectivityQC
    elif ds_type == 'Vel':
        da = dnew2.Velocity
    else:
        pass
    arr = da.to_masked_array(copy=True)
    arr_filled = arr.filled()
    return arr_filled,lats,lons


def calc_dlatlon_dt(starting_coords,starting_time,ending_coords,ending_time):
    """
    One-time calculation of changes in latitude and longitude
    with respect to time to implement feature-following zoom.
    Radar plotting software should be used beforehand to track a 
    feature's lat/lon position at two different scan times
    along with the two different scan times.
    
    This needs to be executed only once at the beginning since 
    dlat_dt and dlon_dt should remain constant.
    
    
    Parameters
    ----------
    starting_coords : tuple containing two floats - (lat,lon)
                      Established with radar plotting software to determine
                      starting coordinates for the feature of interest.

      starting_time : string
                      format - 'yyyy-mm-dd HH:MM:SS' - example - '2018-06-01 22:15:55'

      ending_coords : tuple containing two floats - (lat,lon)
                      Established with radar plotting software to determine
                      starting coordinates for the feature of interest.

        ending_time : string
                      format - 'yyyy-mm-dd HH:MM:SS' - example - '2018-06-01 23:10:05'
                                          
    Returns
    -------
            dlat_dt : float
                      Feature's movement in degrees latitude per second
            dlon_dt : float
                      Feature's movement in degrees longitude per second
                    
    """ 
    starting_datetime = datetime.strptime(starting_time, "%Y-%m-%d %H:%M:%S")
    ending_datetime = datetime.strptime(ending_time, "%Y-%m-%d %H:%M:%S")
    dt =  ending_datetime - starting_datetime
    dt_seconds = dt.seconds
    print('dt_seconds --------- ' + str(dt_seconds))
    dlat_dt = (ending_coords[0] - starting_coords[0])/dt_seconds
    dlon_dt = (ending_coords[1] - starting_coords[1])/dt_seconds

    return dlat_dt, dlon_dt


def make_ticks(this_min,this_max):
    """
    Determines range of tick marks to plot based on a provided range of degree coordinates.
    This function is typically called by 'calc_new_extent' after that function has calculated
    new lat/lon extents for feature-following zoom.
    
    Parameters
    ----------
           this_min : float
                      minimum value of either a lat or lon extent
           this_max : float
                      maximum value of either a lat or lon extent
                                          
    Returns
    -------
           tick_arr : float list
                      list of tick mark labels to use for plotting in the new extent

    """

    t_min = round(this_min) - 0.5
    t_max = round(this_max) + 0.5
    
    t_init = np.arange(t_min,t_max,0.5)    
    tick_arr = []
    for t in range(0,len(t_init)):
        if t_init[t] >= this_min and t_init[t] <= this_max:
            tick_arr.append(t_init[t])
        else:
            pass
    return tick_arr

def calc_new_extent(orig_t,orig_extent,t,lon_rate,lat_rate):
    """

    Shifts the map domain with each image to emulate AWIPS feature following zoom.
    Requires orig_extent [xmin,xmax,ymin,ymax] as a baseline to calculate new_extent

    
    Parameters
    ----------
             orig_t : integer
                      Epoch time (seconds) of first radar product in loop

        orig_extent : list of float
                      xmin, xmax, ymin, ymax
                      
                  t : integer
                      Epoch time (seconds) of current radar product in loop

           lon_rate : float
                      Change of longitude per second wrt time
                      determined ahead of time by 'calc_dlatlon_dt' function

           lat_rate : float
                      Change of latitude per second wrt time
                      determined ahead of time by 'calc_dlatlon_dt' function
                                          
    Returns
    -------
         new_extent : list of floats
                      [min longitude, max longitude, min latitude, max latitude]

             xticks : list of floats
                      list of longitude ticks to plot

             xticks : list of floats
                      list of latitude ticks to plot
                    
    """    
    time_shift = t - orig_t
    lon_shift = time_shift * lon_rate
    lat_shift = time_shift * lat_rate

    xmin = orig_extent[0]
    xmax = orig_extent[1]
    ymin = orig_extent[2]
    ymax = orig_extent[3]    
    new_xmin = xmin + lon_shift
    new_xmax = xmax + lon_shift
    new_ymin = ymin + lat_shift
    new_ymax = ymax + lat_shift
    new_extent = [new_xmin,new_xmax,new_ymin,new_ymax]
    #call 'make_ticks' function to create ticks for new extent
    x_ticks = make_ticks(new_xmin,new_xmax)
    y_ticks = make_ticks(new_ymin,new_ymax)

    return new_extent,x_ticks,y_ticks


def calc_srv(da_v,storm_dir,storm_speed):
    """
    Subtracts storm motion from velocity bin values. This is based on the cosine of the angle
    between the storm direction and a given array radial direction.
    
    Example...
        storm_dir,storm_speed : 250,30 
                 storm motion : from 250 degrees at 30 knots
             max added amount : 30 kts at array's 70 degree radial
        max subtracted amount : 30 kts at array's 250 degree radial             
    
    Parameters
    ----------
                   da_v : xarray
                          velocity velocity data array that will be recalculated
              storm_dir : float
                          storm motion direction in compass degrees
            storm_speed : integer or float
                          storm speed in knots
                    
    Returns
    -------
                srv_arr : numpy masked array of srv floats 
                          
    """
    da_srv = da_v
    # Storm motion is given as a "from" direction, so have to flip
    # this 180 degrees (equal to "pi" radians) to be consistent with
    # radial "to" direction convention
    storm_dir = math.radians(storm_dir) - math.pi

    for a in range(0,len(da_srv.Azimuth)):
        angle = math.radians(da_srv.Azimuth.values[a]) - storm_dir
        factor = math.cos(angle) * storm_speed
        da_srv[a] = da_srv[a] - factor 

    srv_arr = da_srv.to_masked_array(copy=True)

    return srv_arr


def figure_timestamp(dt):
    """
    Creates user-friendly time strings from Unix Epoch Time:
    https://en.wikipedia.org/wiki/Unix_time
    
    Parameters
    ----------
    dt : datetime object
         can also be an int or a string of an int with the proper syntax, in which case it'll be converted
        
    Returns
    -------
    fig_title_timestring    : 'DD Mon YYYY  -  HH:MM:SS UTC'  
    fig_filename_timestring : 'YYYYMMDD-HHMMSS'
                    
    """    
    if type(dt) is not datetime:
        t = datetime.fromtimestamp(dt, timezone.utc)
    else:
        t = dt

    fig_title_timestring = datetime.strftime(t, "%d %b %Y  -  %H:%M:%S %Z")
    fig_filename_timestring = datetime.strftime(t, "%Y%m%d-%H%M%S")
    return fig_title_timestring,fig_filename_timestring

def build_html(image_dir):
    im_dir = pathlib.PurePath(image_dir)
    e_date = im_dir.parts[2]
    if im_dir.parts[3] == 'satellite':
        page_title = e_date + ' satellite'
        loop_description = 'Satellite and Lightning<br>'
    else:
        e_radar = im_dir.parts[3]
        e_slice = im_dir.parts[-1]
        e_slice = e_slice[0:2] + '.' + e_slice[2:4]
        if e_slice[0] == '0':
            e_slice = e_slice[1:]
        page_title = e_date + ' ' + e_radar + ' - ' + e_slice + ' deg'
        loop_description = 'Radar Velocity products derived with WDSS-II  (<a href="http://www.wdssii.org" target="_blank">http://www.wdssii.org/</a>)<br>'
    
    # following file has to be copied into image directory
    # available at https://github.com/tjturnage/resources for download
    # if not manually putting into image directory, will need to note its location and execute the following
    # two commands
    js_src = 'C:/data/scripts/resources/hanis_min.js'
    #js_src = '/data/scripts/resources/hanis_min.js'
    shutil.copyfile(js_src,os.path.join(image_dir,'hanis_min.js'))
    
    # there will be an index.html file created in the image directory to be subsequently opened in an internet browser
    index_path = os.path.join(image_dir,'index.html')
    these_files = os.listdir(image_dir)
    
    # build list of image filenames
    file_str = ''
    for f in (these_files):
        if (re.search('png',f) is not None) or (re.search('png',f) is not None):
            file_str = file_str + f + ', ' 
    
    #trim unwanted characters from string
    file_str = file_str[0:-2]
    
    # first part of html code
    html_1 = '<!doctype html>\
    <html>\
    <head>\
    <meta charset="utf-8">\
    <title>' + page_title + '</title>\
    <script type="text/javascript" src="hanis_min.js"></script>\
    <style>\
    body {\
    	background-color: #434343;\
    	color: white;\
    	font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;\
    	font-size: 12px;\
    	text-align: center;\
    }\
    #container {\
    	position: relative;\
    	width: 1500px;\
     	margin: 0 auto 0 auto;\
    }\
    #hanis {\
    	background-color: #AEAEAE;\
    }\
    a, a:link, a:visited {\
    	color: lightblue;\
    }\
    a:hover {\
    	color: lightgreen;\
    }\
    </style>\
    </head>\
    \
    <body onload="HAniS.setup(\'filenames = '
    
    """
    Example of filenames list...
    ('filenames = 'HRRRMW_prec_radar_000.png, HRRRMW_prec_radar_001.png, HRRRMW_prec_radar_002.png, HRRRMW_prec_radar_003.png, HRRRMW_prec_radar_004.png, HRRRMW_prec_radar_005.png, HRRRMW_prec_radar_006.png, HRRRMW_prec_radar_007.png, HRRRMW_prec_radar_008.png, HRRRMW_prec_radar_009.png, HRRRMW_prec_radar_010.png, HRRRMW_prec_radar_011.png, HRRRMW_prec_radar_012.png, HRRRMW_prec_radar_013.png, HRRRMW_prec_radar_014.png, HRRRMW_prec_radar_015.png, HRRRMW_prec_radar_016.png, HRRRMW_prec_radar_017.png, HRRRMW_prec_radar_018.png\ncontrols = startstop, speed, step, looprock, zoom\ncontrols_style = display:flex;flex-flow:row;\nbuttons_style = flex:auto;margin:2px;cursor:pointer;\nbottom_controls = toggle\ntoggle_size = 8,8,2\ndwell = 100\npause = 1000','hanis')">
    """
    
    file_line_end = '\\ncontrols = startstop, speed, step, looprock, zoom\\ncontrols_style = display:flex;flex-flow:row;\\nbuttons_style = flex:auto;margin:2px;cursor:pointer;\\nbottom_controls = toggle\\ntoggle_size = 8,8,2\\ndwell = 100\\npause = 1000\',\'hanis\')">\
      <div id="container">\
        <div id="hanis"></div>\
        <p>' + loop_description + '\n\
          Velocity products developed by CIMMS (<a href="https://cimms.ou.edu/" target_="blank">https://cimms.ou.edu/</a>) / NSSL (<a href="https://www.nssl.noaa.gov/" target="_blank">https://www.nssl.noaa.gov/</a>) group and are experimental<br>Animation javascript developed by Tom Whittaker (<a href="http://www.ssec.wisc.edu/hanis/">http://www.ssec.wisc.edu/hanis/</a>)\
        </p>\
      </div>\
    </body>\
    </html>'
    
    full_html = html_1 + file_str + file_line_end
    
    f = open(index_path,'w')
    f.write(full_html)
    f.close()
    return

def ltg_plot(highlow,ltg,a):
    """
    Plots lightning and assigns +/ based on polarity and color codes based
    on ground stikes versus height of intercloud flash
    
    Parameters
    ----------
    highlow : string to say whether we're plotting low or high
        ltg : pandas dataframe containing strike data
          a:  matplotlib figure pane in which to create scatterplot
        
    Returns
    -------
    Nothing, just makes a scatterplot then exits
                    
    """    
    for st in range(0,len(ltg)):
        lat = ltg.latitude.values[st]
        lon = ltg.longitude.values[st]
        cur = ltg.peakcurrent[st]
        hgt = ltg.icheight[st]    
        size_add = 0
        if hgt == 0:
            col = 'r'
            size_add = 10
            zord = 10
        elif hgt < 10000:
            col = 'm'
            size_add = 5
            zord = 5
        elif hgt < 15000:
            col = 'c'
            zord = 3            
        elif hgt < 20000:
            col = 'b'
            zord = 2 
        else:
            col = 'g'
            zord = 1 
        if cur > 0:
            symb = '+'
        else:
            symb = '_'
        size = 10 + size_add
        if highlow == 'low' and hgt == 0:    
            a.scatter(lon,lat,s=size,marker=symb,c=col,zorder=zord)
            a.set_title('EN Cloud to Ground')
        elif highlow == 'high' and hgt > 0:
            a.scatter(lon,lat,s=size,marker=symb,c=col,zorder=zord)
            a.set_title('EN Intracloud')
    return

def plot_settings():
    SMALL_SIZE = 8
    MEDIUM_SIZE = 10
    BIGGER_SIZE = 12
    BIGGEST_SIZE = 14
    plt.rc('font', size=BIGGEST_SIZE)          # controls default text sizes
    plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
    plt.rc('axes', labelsize=BIGGER_SIZE)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=BIGGER_SIZE)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
    plt.rc('figure', titlesize=20)  # fontsize of the figure title
    return

class GridShader():
    def __init__(self, ax, first=True, **kwargs):
        self.spans = []
        self.sf = first
        self.ax = ax
        self.kw = kwargs
        self.ax.autoscale(False, axis="x")
        self.cid = self.ax.callbacks.connect('xlim_changed', self.shade)
        self.shade()
    def clear(self):
        for span in self.spans:
            try:
                span.remove()
            except:
                pass
    def shade(self, evt=None):
        self.clear()
        xticks = self.ax.get_xticks()
        xlim = self.ax.get_xlim()
        xticks = xticks[(xticks > xlim[0]) & (xticks < xlim[-1])]
        locs = np.concatenate(([[xlim[0]], xticks, [xlim[-1]]]))

        start = locs[1-int(self.sf)::2]  
        end = locs[2-int(self.sf)::2]

        for s, e in zip(start, end):
            self.spans.append(self.ax.axvspan(s, e, zorder=0, **self.kw))