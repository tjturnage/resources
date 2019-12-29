# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 20:39:16 2019

@author: tjtur
"""

import os
import requests
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

def str_to_fl(string):
    """
    Takes string as input and attempts to convert to float.
    If unsuccessful, returns 'NA' string
    """
    try:
        return float(string)
    except:
        return 'NA'

def mesowest_data_from_latest_observation(dataframe,pd_time,station):
    """
    Identifies the most recent observation in a dataframe sliced by time and station.
    Returns the values
    
    Parameters
    ----------
          dataframe : pandas dataframe from which a slice will be taken  
            pd_time : pandas datetime that's used to slice off all preceeding data
         slice_type : mesowest station for which latest observation time will be determined
                                          
    Returns
    -------
           stn_data : list
                      extacts metadata and (t,dp,wdir,wspd,wgust) from latest observation using '.max()'
                      calls 'str_to_flt' function to convert number strings to floats
                      if (t,dp,wdir,wspd) all exist
                         returns list of data values associated with 
                      otherwise returns nothing

 
    """
    #print(pd_time,station)#new_data = sfc_D[slice_info][-1:]
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
    
def mesowest_get_timeseries(start_time,end_time,stns,fout):
    with open(fout,'w') as fout:
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

def mesowest_get_current_observations():
    stns_list = []
    #mini_list = []
    #varStr = 'air_temp,dew_point_temperature,wind_speed,wind_direction'
    api_arguments = {"token":API_TOKEN,"radius":"KLDM,100", "status":"active","network":"1,2,96", "vars": varStr}
    #api_arguments = {"token":API_TOKEN,"stid":"2465", "network":"1,2,96", "vars": varStr}
    api_request_url = os.path.join(API_ROOT, "stations/latest")
    req = requests.get(api_request_url, params=api_arguments)
    jas2 = req.json()
    for s in range(0,len(jas2['STATION'])):
        try:
            station = jas2['STATION'][s]
            stn_id = station['STID']
            print(stn_id)
            #mnet_id = station['MNET_ID']
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
        except:
            pass
    print(stns_list)
    return jas2,stns_list,line
