# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 20:39:16 2019

@author: tjtur
"""

import os
import sys
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


varStr = 'air_temp,dew_point_temperature,wind_speed,wind_direction,wind_gust,visibility,road_temp'
unitsStr = 'temp|F,speed|kts,precip|in'  
API_ROOT = "https://api.synopticdata.com/v2/"
API_TOKEN = "292d36a692d74badb6ca011f4413ae1b"

shortDict = {'air_temp_value_1':'t',
             'dew_point_temperature_value_1d':'dp',
             'wind_speed_value_1':'wspd',
             'wind_direction_value_1':'wdir',
             'wind_gust_value_1':'wgst',
             'visibility_value_1':'vis'}

#class Mesowest():
#    def __init__(self,timeStr):
#
#
#        def str_to_fl(string):
#            """
#            Takes string as input and attempts to convert to float.
#            If unsuccessful, returns 'NA' string
#            """
#            try:
#                return float(string)
#            except:
#                return 'NA'
        
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
                      string of number to be used to reference placefile icon

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

def convertVal(num,short):
    """
    converts units based on variable type
    Probably needs to be replaced by metpy methods at some point
    """
    numfloat = float(num)
    if (num != 'NA' ):
        if (short == 't') or (short == 'dp') or (short == 'rt'):
            new = (numfloat * 9.0/5.0) + 32.0
            newStr = '" ' + str(int(round(new))) + ' "'
        elif short == 'vis':
            new = numfloat
            newStr = '" ' + str(new) + ' "'        
        elif short == 'wspd':
            scratch = numfloat * 1.944
            new = placefileWindSpeedCode(scratch)
            newStr = str(new)
        elif short == 'wdir':
            new = int(num)
            newStr = str(new)

        return newStr, new


"""
class Mesowest:
    def __init__(self, radar, timeStr,stid, elements, units, archive=False):

        self.timeStr = timeStr
        self.stid = stid
        self.radar = radar
        self.elements = elements
        
        API_ROOT = "https://api.synopticdata.com/v2/"
        API_TOKEN = "292d36a692d74badb6ca011f4413ae1b"

        placeHead = 'Title: Mesowest Obs ' + timeStr + '\nRefresh: 2\nColor: 255 200 255\n \
        IconFile: 1, 18, 32, 2, 31, "https://mesonet.agron.iastate.edu/request/grx/windbarbs.png" \n \
        IconFile: 2, 15, 15, 8, 8, "https://mesonet.agron.iastate.edu/request/grx/cloudcover.png"\n \
        IconFile: 3, 25, 25, 12, 12, "https://mesonet.agron.iastate.edu/request/grx/rwis_cr.png"\n \
        Font: 1, 14, 1, "Arial"\n\n'

        shortDict = {'air_temp_value_1':'t',
                     'dew_point_temperature_value_1d':'dp',
                     'wind_speed_value_1':'wspd',
                     'wind_direction_value_1':'wdir',
                     'wind_gust_value_1':'wgst',
                     'visibility_value_1':'vis'}


        stnDict2 = {'t':{'threshold':100,'color':'200 100 100','position':'-17,13, 1,'},
                  'dp':{'threshold':100,'color':'0 255 0','position':'-17,-13, 1,'},
                  'wspd':{'threshold':500,'color':'255 255 255','position':'NA'},
                  'wdir':{'threshold':500,'color':'255 255 255','position':'NA'},
                  'wgst':{'threshold':300,'color':'255 255 255','position':'NA'},
                  'vis':{'threshold':125,'color':'180 180 255','position':'17,-13, 1,'},
                  'rt':{'threshold':125,'color':'255 255 0','position':'17,13, 1,'}}
        
        nowTime = datetime.utcnow()
        time_str = datetime.strftime(nowTime,'%Y%m%d%H%M')



        if archive:
            api_arguments = {"token":API_TOKEN,"state":"mi","network":"1,2,71,96,162,3001", "vars": elements, "units": units, 'attime': time_str, 'within':'30' }
            #api_arguments = {"token":API_TOKEN,"cwa":"bmx", "vars": varStr, "units": unitsStr, 'attime': timeStr, 'within':'40' }
            api_request_url = os.path.join(API_ROOT, "stations/nearesttime")
        else:
            api_arguments = {"token":API_TOKEN,"stid":stid, "vars": elements, "units": units}
            api_request_url = os.path.join(API_ROOT, "stations/latest")
    
        req = requests.get(api_request_url, params=api_arguments)
        jas = req.json()


        self.wdir = jas['STATION'][0]['OBSERVATIONS']['wind_direction_value_1']['value']
        self.wspd = jas['STATION'][0]['OBSERVATIONS']['wind_speed_value_1']['value']
        self.lat = jas['STATION'][0]['LATITUDE']
        self.lon = jas['STATION'][0]['LONGITUDE']
        self.wind_str = f'{self.wdir:.0f}/{self.wspd:.0f}'
        self.archive_fname = radar + '_' + time_str + '.png'
        self.archive_fpath = os.path.join(archive_dir,self.archive_fname)
        self.current_fname = radar + '.png'
        self.current_fpath = os.path.join(image_dir,self.current_fname)

        self.cmd_str = py_call + vwp_script_path + ' ' + radar + ' -s ' + self.wind_str + ' -f ' + self.archive_fpath + ' -x'



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

        @classmethod
        def vwp(cls,wdir,wspd,radar,stid):
            nowTime = datetime.utcnow()
            time_str = datetime.strftime(nowTime,'%Y%m%d%H%M')
            cls.obtime_str = time_str
            cls.wdir = wdir
            cls.wspd = wspd        
            cls.stid = stid
            cls.radar = radar
            cls.elements = 'wind_speed,wind_direction,wind_gust'
            cls.units = 'speed|kts,precip|in'
    
    
    
            @classmethod
            def placefileWindSpeedCode(cls,wspd):
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
        
            @classmethod    
            def windDir(cls,wdir):
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
    
            @classmethod 
            def convertVal(cls,num,short):
                numfloat = float(num)
                if (num != 'NA' ):
                    if (short == 't') or (short == 'dp') or (short == 'rt'):
                        new = (numfloat * 9.0/5.0) + 32.0
                        newStr = '" ' + str(int(round(new))) + ' "'
                    elif short == 'vis':
                        new = numfloat
                        newStr = '" ' + str(new) + ' "'        
                    elif short == 'wspd':
                        scratch = numfloat * 1.944
                        new = placefileWindSpeedCode(scratch)
                        newStr = str(new)
                    elif short == 'wdir':
                        new = int(num)
                        newStr = str(new)
            
                    return newStr, new
"""