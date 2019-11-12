# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 16:48:37 2019

@author: thomas.turnage
"""



state2timezone = { 'AK': 'US/Alaska', 'AL': 'US/Central', 'AR': 'US/Central', 'AS': 'US/Samoa',
                  'AZ': 'US/Mountain', 'CA': 'US/Pacific', 'CO': 'US/Mountain', 'CT': 'US/Eastern',
                  'DC': 'US/Eastern', 'DE': 'US/Eastern', 'FL': 'US/Eastern', 'GA': 'US/Eastern',
                  'GU': 'Pacific/Guam', 'HI': 'US/Hawaii', 'IA': 'US/Central', 'ID': 'US/Mountain', 
                  'IL': 'US/Central', 'IN': 'US/Eastern', 'KS': 'US/Central', 'KY': 'US/Eastern',
                  'LA': 'US/Central', 'MA': 'US/Eastern', 'MD': 'US/Eastern', 'ME': 'US/Eastern',
                  'MI': 'US/Eastern', 'MN': 'US/Central', 'MO': 'US/Central', 'MP': 'Pacific/Guam', 
                  'MS': 'US/Central', 'MT': 'US/Mountain', 'NC': 'US/Eastern', 'ND': 'US/Central', 
                  'NE': 'US/Central', 'NH': 'US/Eastern', 'NJ': 'US/Eastern', 'NM': 'US/Mountain', 
                  'NV': 'US/Pacific', 'NY': 'US/Eastern', 'OH': 'US/Eastern', 'OK': 'US/Central', 
                  'OR': 'US/Pacific', 'PA': 'US/Eastern', 'PR': 'America/Puerto_Rico', 
                  'RI': 'US/Eastern', 'SC': 'US/Eastern', 'SD': 'US/Central', 'TN': 'US/Central', 
                  'TX': 'US/Central', 'UT': 'US/Mountain', 'VA': 'US/Eastern', 'VI': 'America/Virgin',
                  'VT': 'US/Eastern', 'WA': 'US/Pacific', 'WI': 'US/Central',
                  'WV': 'US/Eastern', 'WY': 'US/Mountain', '' : 'US/Pacific', '--': 'US/Pacific' }

time_shift_dict = {'US/Eastern':4,'US/Central':5,'US/Mountain':6,'US/Pacific':7,'US/Hawaii':7,
                   'US/Alaska':8,'Pacific/Guam':9, 'America/Puerto_Rico':3,'America/Virgin':3}

def nbm_station_dict():
    fin = 'C:/data/scripts/NBM/NBM_stations.txt'
    station_master = {}
    with open(fin,'r') as src:
        for line in src:
            elements = line.split(',')
            station_id = str(elements[0])
            station_name = str(elements[1])
            state = str(elements[2])
            if state in state2timezone.keys():
                lat = float(elements[3])
                lon = float(elements[4])
                utc_shift = time_shift_dict[state2timezone[state]]
                #print(station,state,lat,lon,time_shift_dict[utc_shift])
                #station_info[station] = ([('state', state) , ('utc_shift', time_shift_dict[utc_shift]) ,('lat', lat) , ('lon' , 20)] )
                #station_master[station] = ([('state',state),('time_shift',utc_shift),('lat',lat),('lon',lon)])
                station_master[station_id] = ({'name':station_name,'state':state,'time_shift':utc_shift,'lat':lat,'lon':lon})
    
            else:
                utc_shift = 0
        
        return station_master