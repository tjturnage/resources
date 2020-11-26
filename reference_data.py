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

# Daylight time commented out
#time_shift_dict = {'US/Eastern':4,'US/Central':5,'US/Mountain':6,'US/Pacific':7,'US/Hawaii':7,
#                   'US/Alaska':8,'Pacific/Guam':9, 'America/Puerto_Rico':3,'America/Virgin':3}

time_shift_dict = {'US/Eastern':5,'US/Central':6,'US/Mountain':7,'US/Pacific':8,'US/Hawaii':9,
                   'US/Alaska':9,'Pacific/Guam':10, 'America/Puerto_Rico':4,'America/Virgin':4}

import os
import sys

def set_paths():
    
    try:
        os.listdir('/usr')
        data_dir = '/data'
        scripts_dir = os.path.join(data_dir,'scripts')
        sys.path.append(os.path.join(scripts_dir,'resources'))
        image_dir = os.path.join('/var/www/html','images')
        placefile_dir = os.path.join('/var/www/html','placefiles')
        archive_dir = os.path.join(image_dir,'archive')
        gis_dir = os.path.join(data_dir,'GIS')
        py_call = '/usr1/anaconda3/bin/python '

    except:
        data_dir = 'C:/data'    
        scripts_dir = os.path.join(data_dir,'scripts')
        sys.path.append(os.path.join(scripts_dir,'resources'))
        image_dir = os.path.join(data_dir,'images')
        placefile_dir = os.path.join(data_dir,'placefiles')
        archive_dir = os.path.join(data_dir,'archive')
        gis_dir = os.path.join(data_dir,'GIS')
        py_call = None

    
    return data_dir,image_dir,archive_dir,gis_dir,py_call,placefile_dir


def set_basic_paths():
    
    try:
        os.listdir('/usr')
        data_dir = '/data'
        scripts_dir = os.path.join(data_dir,'scripts')
        sys.path.append(os.path.join(scripts_dir,'resources'))
        image_dir = os.path.join('/var/www/html','images')

    except:
        data_dir = 'C:/data'    
        scripts_dir = os.path.join(data_dir,'scripts')
        sys.path.append(os.path.join(scripts_dir,'resources'))
        image_dir = os.path.join(data_dir,'images')


    
    return data_dir,scripts_dir,image_dir