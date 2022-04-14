# -*- coding: utf-8 -*-
"""

05 Jan 2020: Now importing API_TOKEN for privacy since data are proprietary

             Learn more about setting up your own account at:
                 https://synopticdata.com/


"""

import os
import sys
import math
import requests
from datetime import datetime, timedelta

try:
    os.listdir('/usr')
    scripts_dir = '/data/scripts'
    sys.path.append(os.path.join(scripts_dir,'resources'))
except:
    scripts_dir = 'C:/data/scripts'
    sys.path.append(os.path.join(scripts_dir,'resources'))

from reference_data import set_paths
data_dir,image_dir,archive_dir,gis_dir,py_call,placefile_dir = set_paths()
vwp_script_path = os.path.join(scripts_dir,'vad-plotter-master','vad.py')

class Mesowest(network="1,2,96"):
    def __init__(self):
        "state":"ia,mn,ne,ks,wi,mo"
        "network":"1,2,71,96,162,3001", "vars": varStr, "units": unitsStr, 'attime': timeStr, 'within':'30'


varStr = 'air_temp,dew_point_temperature,wind_speed,wind_direction,wind_gust,visibility,road_temp'
unitsStr = 'temp|F,speed|kts,precip|in'  
API_ROOT = "https://api.synopticdata.com/v2/"
from api_tokens import mesowest_API_TOKEN as API_TOKEN
#from api_tokens import mPING_API_TOKEN
#https://mping.ou.edu/api/

shortDict = {'air_temp_value_1':'t',
             'dew_point_temperature_value_1d':'dp',
             'wind_speed_value_1':'wspd',
             'wind_direction_value_1':'wdir',
             'wind_gust_value_1':'wgst',
             'visibility_value_1':'vis'}

stnDict2 = {'t':{'threshold':300,'color':'200 100 100','position':'-17,13, 1,'},
          'dp':{'threshold':300,'color':'0 255 0','position':'-17,-13, 1,'},
          'wspd':{'threshold':500,'color':'255 255 255','position':'NA'},
          'wdir':{'threshold':500,'color':'255 255 255','position':'NA'},
          'wgst':{'threshold':300,'color':'255 255 255','position':'NA'},
          'vis':{'threshold':100,'color':'180 180 255','position':'17,-13, 1,'},
          'rt':{'threshold':125,'color':'255 255 0','position':'17,13, 1,'}}

   
def str_to_fl(string):
    """
    Takes string as input and attempts to convert to float.
    If unsuccessful, returns 'NA' string
    """
    try:
        return float(string)
    except:
        return 'NA'



def mesowest_get_current_observations(radius_str="KLDM,100",network="1,2,96"):
    """
    Retrieves newest observations via the Mesowest API. API Documentation at:
    https://developers.synopticdata.com/mesonet/v2/stations/latest/
    
    Parameters
    ----------

         radius_str : Documentation about radius at:
                      https://developers.synopticdata.com/mesonet/v2/station-selectors/
            network : list of network/station providers to be used. Documentation at:
                      https://developers.synopticdata.com/about/station-providers                                          
    Returns
    -------
               jas2 : json file
                      Dictionary of metadata and observations for all stations within radius
          stns_list : list
                      list of ids of the stations that had data retrieved successfully
 
    """
    stns_list = []
    varStr = 'air_temp,dew_point_temperature,wind_speed,wind_direction'
    api_arguments = {"token":API_TOKEN,"radius":radius_str, "status":"active","network":"1,2,96", "vars": varStr}
    #api_arguments = {"token":API_TOKEN,"radius":"KLDM,100", "status":"active","network":"1,2,96", "vars": varStr}
    #api_arguments = {"token":API_TOKEN,"stid":"2465", "network":"1,2,96", "vars": varStr}
    api_request_url = os.path.join(API_ROOT, "stations/latest")
    req = requests.get(api_request_url, params=api_arguments)
    jas2 = req.json()
    for s in range(0,len(jas2['STATION'])):
        try:
            station = jas2['STATION'][s]
            stn_id = station['STID']
            print(stn_id)
            stns_list.append(str(stn_id))
            lat = station['LATITUDE']
            lon = station['LONGITUDE']        
            ob_time = station['OBSERVATIONS']['wind_gust_value_1']['date_time']
            wgst = station['OBSERVATIONS']['wind_gust_value_1']['value']
            wdir = station['OBSERVATIONS']['wind_direction_value_1']['value']
            wspd = station['OBSERVATIONS']['wind_speed_value_1']['value']
            dwpt = station['OBSERVATIONS']['dew_point_temperature_value_1d']['value']
            temp = station['OBSERVATIONS']['air_temp_value_1']['value']
            print(stn_id)
            line = ([stn_id,ob_time,lat,lon,temp,dwpt,wdir,wspd,wgst])
            print(line)
        except:
            pass

    return jas2,stns_list

    
def mesowest_get_timeseries(start_time,end_time,stns_list,dst_file):
    """
    For each station in a list of stations, retrieves all observational data within a defined
    time range using mesowest API. Writes the retrieved data and associated observation times
    to a destination file. API documentation:
    
        https://developers.synopticdata.com/mesonet/v2/stations/timeseries/
    
    Parameters
    ----------
         start_time : string 
                      data start time to be passed to the mesowest API
                      format - YYYYMMDDhhmm
                      
           end_time : string 
                      data end time to be passed to the mesowest API
                      format - YYYYMMDDhhmm
               
          stns_list : list
                      stations that will have time series data requested
                      This can either be a pre-staged list or can come from 
                      mesowest_get_current_observations function
                      
           dst_file : Path to file that will be written to with 
                    

                                          
    Returns
    -------
             jas_ts : json file
                      dictionary of all observations for a given station
                      
                      What is most significant, however, is writing the observed data
                      to a file that then can be manipulated for plotting
 
    """
    stns = ','.join(stns_list)
    with open(dst_file,'w') as fout:
    #stn_data = []
        api_arguments = {"token":API_TOKEN,"stid":stns,"start":start_time ,"end":end_time ,"vars": varStr, "units": unitsStr}
        api_request_url = os.path.join(API_ROOT, "stations/timeseries")
        req = requests.get(api_request_url, params=api_arguments)
        jas_ts = req.json()
        for s in range(0,len(jas_ts['STATION'])):
            try:
                station = jas_ts['STATION'][s]
                stn_id = station['STID']
                print(stn_id)
                lat = station['LATITUDE']
                lon = station['LONGITUDE']        
                ob_times = station['OBSERVATIONS']['date_time']
                print(ob_times)

                wgsts = station['OBSERVATIONS']['wind_gust_set_1']
                wdirs = station['OBSERVATIONS']['wind_direction_set_1']
                wspds = station['OBSERVATIONS']['wind_speed_set_1']
                dwpts = station['OBSERVATIONS']['dew_point_temperature_set_1d']
                temps = station['OBSERVATIONS']['air_temp_set_1']
                for dt in range(0,len(ob_times)):
                    line = ','.join([ob_times[dt][:-1],stn_id,lat,lon,str(temps[dt]),str(dwpts[dt]),str(wdirs[dt]),str(wspds[dt]),str(wgsts[dt])])
                    print(line)
                    fout.write(line + '\n')
            except:
                pass
        return jas_ts


def mesowest_data_from_latest_observation(dataframe,pd_time,station):
    """
    Identifies the most recent observation in a dataframe sliced by time and station.
    Returns those values
    
    Parameters
    ----------
          dataframe : pandas dataframe from which a slice will be taken  
            pd_time : pandas datetime that's used to slice off all preceeding data
            station : string 
                      mesowest station id for which latest observation time will be determined
                                          
    Returns
    -------
           stn_data : list
                      extacts metadata and (t,dp,wdir,wspd,wgust) from latest observation using '.max()'
                      calls 'str_to_flt' function to convert number strings to floats
                      if (t,dp,wdir,wspd) all exist
                         returns list of data values associated with the observation
                      otherwise returns nothing

 
    """

    sfc_D = dataframe
    new_data = None
    try:
        new_data = sfc_D[(sfc_D.index < pd_time) & (sfc_D.station_id == station)]
        new_data_max = new_data[new_data.index == new_data.index.max()]
        index_time = pd_time.strftime('%Y%m%d%H%M')
        ob_time = new_data_max.index[0].strftime('%Y%m%d%H%M')
        lat = str_to_fl(new_data_max.lat.values[-1])
        lon = str_to_fl(new_data_max.lon.values[-1])
        t = str_to_fl(new_data_max.temp.values[-1])    
        dp = str_to_fl(new_data_max.dewpoint.values[-1])
        wdir = str_to_fl(new_data_max.wdir.values[-1])   
        wspd = str_to_fl(new_data_max.wspd.values[-1])
        wgst = str_to_fl(new_data_max.wgst.values[-1])
        #data_path = new_data.file_path.max()
        stn_data = [station,index_time,ob_time,lat,lon,t,dp,wdir,wspd,wgst]
        if 'NA' not in (t,dp,wdir,wspd):
            return stn_data
        else:
            return None
    except:
        return None

def mesowest_get_nearest_time_data(timeStr):
    """
    Returns data from the mesowest API corresponding to the nearest available
    time associated with a time string.
    
    Parameters
    ----------
            timeStr : string
                      format is YYYYmmDDHHMM (ex. 202002290630)
                                        
    Returns
    -------
               code : json file
                      observational data
    
    Future work - pass api_arguments to function instead of hard-wiring

    """
    api_arguments = {"token":API_TOKEN,"state":"ia,mn,ne,ks,wi,mo","network":"1,2,71,96,162,3001", "vars": varStr, "units": unitsStr, 'attime': timeStr, 'within':'30' }
    api_request_url = os.path.join(API_ROOT, "stations/nearesttime")
    req = requests.get(api_request_url, params=api_arguments)
    jas = req.json()
    return jas

def timeShift(dt,num):
    times = []
    origTime = datetime.strptime(dt,'%Y%m%d%H%M')
    steps = int(num)
    for x in range(0,steps):
        mins = x * 15
        origTime = origTime + timedelta(minutes=mins)
        forTime = origTime + timedelta(minutes=15)
        origStr = datetime.strftime(origTime, '%Y%m%d%H%M.txt')
        orig = datetime.strftime(origTime, '%Y-%m-%dT%H:%M:%SZ')
        forward = datetime.strftime(forTime, '%Y-%m-%dT%H:%M:%SZ')
        times.append([origStr,orig,forward])
    return times


def placefileWindSpeedCode(wspd):
    """
    Returns the proper code for plotting wind speeds in a GR2Analyst placefile. 
    This code is then used for the placefile IconFile method described at:
        http://www.grlevelx.com/manuals/gis/files_places.htm
    
    Parameters
    ----------
               wspd : string
                      wind speed in knots
                                        
    Returns
    -------
               code : string
                      string of integer to be used to reference placefile icon

    """
    speed = float(wspd)
    if speed > 52:
        code = '11'
    elif speed > 47:
        code = '10'
    elif speed > 42:
        code = '9'
    elif speed > 37:
        code = '8'
    elif speed > 32:
        code = '7'
    elif speed > 27:
        code = '6'
    elif speed > 22:
        code = '5'
    elif speed > 17:
        code = '4'
    elif speed > 12:
        code = '3'
    elif speed > 7:
        code = '2'
    elif speed > 2:
        code = '1'
    else:
        code = '1'
    
    return code
    
    
def windDir(wdir):
    """
    Returns the proper code for plotting wind speeds in a GR2Analyst placefile. 
    This code is then used for the placefile IconFile method described at:
        http://www.grlevelx.com/manuals/gis/files_places.htm
    
    Parameters
    ----------
               wspd : string
                      wind speed in knots
                                        
    Returns
    -------
               code : string
                      string of integer to be used to reference placefile icon

    """

    wd = int(wdir)
    if wd < 20:
        wc = 'N'    
    elif wd < 75:
        wc = 'NE'
    elif wd < 115:
        wc = 'E'
    elif wd < 155:
        wc = 'SE'
    elif wd < 200:
        wc = 'S'
    elif wd < 250:
        wc = 'SW'
    elif wd < 290:
        wc ='W'
    elif wd < 340:
        wc = 'NW'
    else:
        wc = 'N'

    return wd,wc        



def convert_met_values(num,short):
    numfloat = float(num)
    if (num != 'NA' ):
        if (short == 't') or (short == 'dp') or (short == 'rt'):
            new = int(round(numfloat))
            newStr = '" ' + str(new) + ' "'
            textInfo = buildObject(newStr,short)
        elif short == 'wgst':
            new = int(round(numfloat,1))
            newStr = '" ' + str(new) + ' "'        
            textInfo = buildObject(newStr,short)
            newStr = str(new)
        elif short == 'vis':
            #print (numfloat)
            final = '10'
            if numfloat < 6.5:
                final = str(int(round(numfloat)))
            if numfloat <= 2.75:
                final = '2 3/4'
            if numfloat <= 2.50:
                final = '2 1/2'                
            if numfloat <= 2.25:
                final = '2 1/4'
            if numfloat <= 2.0:
                final = '2'
            if numfloat <= 1.75:
                final = '1 3/4'                 
            if numfloat <= 1.50:
                final = '1 1/2'                 
            if numfloat <= 1.25:
                final = '1 1/4'
            if numfloat <= 1.00:
                final = '1'
            if numfloat <= 0.75:
                final = '3/4'                   
            if numfloat <= 0.50:
                final = '1/2'
            if numfloat <= 0.25:
                final = '1/4'
            if numfloat <= 0.125:
                final = '1/8'
            if numfloat == 0.0:
                final = ''
            newStr = '" ' + final + ' "'        
            textInfo = buildObject(newStr,short)
        elif short == 'wspd':
            new = placefileWindSpeedCode(numfloat)
            newStr = str(new)
            textInfo = 'ignore'
        elif short == 'wdir':
            new = int(num)
            newStr = str(new)
            textInfo = 'ignore'

        return newStr, textInfo

def gustObj(wdir, wgst, short):
    wgstInt = int(wgst)
    newStr = '" ' + str(wgstInt) + ' "'
    direction = int(wdir)
    distance = 35
    x = math.sin(math.radians(direction)) * distance
    y = math.cos(math.radians(direction)) * distance
    loc = str(int(x)) + ',' + str(int(y)) + ',1,'
    threshLine = 'Threshold: ' + str(stnDict2[short]['threshold']) + '\n'
    colorLine = '  Color: ' + str(stnDict2[short]['color']) + '\n'
    position = '  Text: ' + loc + newStr + ' \n'
    textInfo = threshLine + colorLine + position
    return textInfo

def buildObject(newStr,short):
    threshLine = 'Threshold: ' + str(stnDict2[short]['threshold']) + '\n'
    colorLine = '  Color: ' + str(stnDict2[short]['color']) + '\n'
    position = '  Text: ' + str(stnDict2[short]['position']) + newStr + '\n'
    textInfo = threshLine + colorLine + position
    return textInfo

