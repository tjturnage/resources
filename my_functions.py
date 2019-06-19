# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 09:33:56 2019

@author: tjtur

List:
    latlon_from_radar
    make_ticks
    calc_new_extent
    calc_srv
    get_shapefile
    figure_timestamp

"""

def latlon_from_radar(az,elevation,num_gates,radar_lat,radar_lon):
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
    rng = None
    factor = math.cos(math.radians(elevation))
    if num_gates <= 334:
        gate_len = 1000.0 * factor
    else:
        gate_len = 250.0 * factor
    rng = np.arange(2125.0,(num_gates*gate_len + 2125.0),gate_len)
    g = Geod(ellps='clrk66')
    center_lat = np.ones([len(az),len(rng)])*radar_lat
    center_lon = np.ones([len(az),len(rng)])*radar_lon
    az2D = np.ones_like(center_lat)*az[:,None]
    rng2D = np.ones_like(center_lat)*np.transpose(rng[:,None])
    lat,lon,back=g.fwd(center_lon,center_lat,az2D,rng2D)
    return lat,lon,back


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


def get_shapefile(shape_path):
    reader = shpreader.Reader(shape_path)
    features = list(reader.geometries())
    SHAPEFILE = cfeature.ShapelyFeature(features, ccrs.PlateCarree())
    return SHAPEFILE


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
        t = datetime.fromtimestamp(int(dt), timezone.utc)
    else:
        t = dt

    fig_title_timestring = datetime.strftime(t, "%d %b %Y  -  %H:%M:%S %Z")
    fig_filename_timestring = datetime.strftime(t, "%Y%m%d-%H%M%S")
    return fig_title_timestring,fig_filename_timestring


import math
import os
from datetime import datetime,timezone
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from pyproj import Geod
import cartopy.io.shapereader as shpreader
