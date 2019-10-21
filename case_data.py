# -*- coding: utf-8 -*-
"""
A collection of dictionaries. Each dictionary contains metadata for a case.
Creating a dictionary for a case is the first in the whole work flow. A dictionary
gets selected with:

    this_case = cases['[letter]']    

That dictionary then gets imported into:

    wdss_create_netcdfs.py          :    make netcdfs for that case
    wdss_stage_files.py             :    copy/rename netcdfs to a staging directory
    wdss_create_figures.py          :    create images using staged netcdfs              
    

A dictionary contains the following case information:

Required:    
         cases : key      : arbitrary name for case
          date : string   : for file/directory naming conventions   
           rda : string   : also for file/directory naming conventions
        latmax : float    : north map plot extent
        latmin : float    : south map plot extent
        lonmin : float    : west map plot extent
        lonmax : float    : east map plot extent
       cutlist : list     : used by wdss_stage_files.py to know which cuts to copy
  
Optional:    
      eventloc : float tuple  : event lat/lon pair to plot as marker 
     eventloc2 : float tuple  : (event lat/lon pair to plot as marker 
  start_latlon : float tuple  : initial lat/lon coordinates of feature
    end_latlon : float tuple  : final lat/lon coordinates of feature
    start_time : string       : product time stamp associated with start_latlon
                              ::  example... '2017-07-20 00:07:34'
      end_time : string       : product time stamp associated with end_latlon
  storm_motion : float tuple  : storm direction in degrees, speed in knots

feature_follow : boolean      : whether figures should be rendered feature follow
     
author: thomas.turnage@noaa.gov
Last updated:
    10 June 2019 - removed lat/lon ticks since make_ticks function in create_figures.py does this now
    11 June 2019 - added 'storm_motion' as input for srv function in create_figures.py
------------------------------------------------
"""

#product_list = ['AzShear_Storm','DivShear_Storm','Velocity_Gradient_Storm','ReflectivityQC','Velocity',
#                'SRV','SpectrumWidth']

cases = {}

cases['20080608_KGRR'] = {'date':'20080608',
     'rda':'KGRR',
     'lonmin':-87.45,
     'lonmax':-85.8,
     'latmin':43.05,
     'latmax':44.35,
     'start_latlon': (43.51,-86.05),
     'end_latlon': (43.05,-84.65),
     'start_time': '2008-06-08 17:47:51',
     'end_time': '2008-06-08 19:42:28',
     'storm_motion': (250,45),
     'feature_follow': True,
     'cutlist': ['00.50'],
     'shapelist':['MI']
     }

cases['20080608_KDTX'] = {'date':'20080608',
     'rda':'KDTX',
     'lonmin':-85.22,  # 1.65 / 2 = 0.65
     'lonmax':-84.0,
     'latmin':42.35,    # 42.8 ... 1.30 / 2 = 0.65
     'latmax':43.30,
     'start_latlon': (42.73,-84.47),
     'end_latlon': (42.74,-84.29),
     'start_time': '2008-06-08 20:04:37',
     'end_time': '2008-06-08 20:13:09',
     'storm_motion': (267,57),
     'feature_follow': True,
     'cutlist': ['00.50','00.90','01.30'],
     'shapelist':['MI']
     }

cases['20170919_KMVX'] = {'date':'20170919',
     'rda':'KMVX',
     'latmax':48.1,
     'latmin':46.05,
     'lonmin':-98.75,
     'lonmax':-96.15,
     'eventloc': (-96.53,47.5452),
     'eventloc2': (-96.5337,47.5401),     
     'start_latlon': (47.31,-96.70),
     'end_latlon': (47.39,-96.65),
     'start_time': '2017-07-20 00:07:34',
     'end_time': '2017-07-20 00:18:01',
     'storm_motion': (211,35),  
     'feature_follow': True,
     'cutlist': ['00.50','00.90','01.30','01.80','02.40'],
     'shapelist':['MN','ND']
     }


cases['20180827_KMVX'] = {'date':'20180827',
     'rda':'KMVX',
     'latmax':48.25,
     'latmin':46.750,
     'lonmin':-97.4,
     'lonmax':-95.5,
     'extent': [-97.4,-95.5,46.75,48.25],
     'storm_motion': (250,55),    
     'eventloc': (-96.12,47.44),
     #'cutlist': ['00.50', '00.90', '01.30'],
     'cutlist': ['01.80', '02.40', '03.10'],
     'shapelist':['MN','ND']
     }

cases['20190314_KDTX'] = {'date':'20190314',
     'rda':'KDTX',
     'lonmin':-84.5,
     'lonmax':-83.35,
     'latmin':42.57,
     'latmax':43.5,
     'start_latlon': (42.87,-84.158),
     'end_latlon': (43.93,-84.035),
     'start_time': '2019-03-14 22:49:33',
     'end_time': '2019-03-14 22:58:17',
     'pandas' : ('2019-06-01 22:15', 24, '5min'),
     'start_figures': 20190314221500,
     'end_figures': 20190314234000,
     'extent': ['lonmin','lonmax''latmin','latmax'],
     'sat_extent' : [-85.0,-83.2,42.0,43.5],
     #'sat_extent' : [-87.4,-81.2,39.75,45.5],
     'storm_motion': (236,45),
     #'eventloc': (-85,19,42.31),
     'feature_follow': False,
     #'eventloc2': (-94.93,39.06),
     'cutlist': ['0.50','0.90','1.30','1.80','2.40'],
     'shapelist':['MI','20190314_survey']
     }

cases['20190519_KGRR'] = {'date':'20190519',
     'rda':'KGRR',
     'lonmin':-85.72,
     'lonmax':-85.17,
     'latmin':42.3,
     'latmax':42.75,
     'eventloc': (-85.17,42.53),
     'extent':[-85.75,-85.0,39.30],
     'start_latlon': (42.43,-85.44),
     'end_latlon': (42.51,-85.246),
     'start_time': '2019-05-19 22:03:39',
     'end_time': '2019-05-19 22:18:11',
     'storm_motion': (240,30),
     'feature_follow': True,
     'products': ['AzShear_Storm','DivShear_Storm'],
     'cutlist': ['00.50', '00.90', '01.30', '01.80', '02.40'],
     'shapelist':['MI']
     }



cases['20190527_KGLD'] = {'date':'20190527',
     'rda':'KGLD',
     'lonmin':-103.00,
     'lonmax':-101.8,
     'latmin':38.05,
     'latmax':39.0,     
     'eventloc': (-102.29,38.59),
     'storm_motion': (200,49),
     'cutlist': ['00.50', '00.90'],
     'shapelist':['CO','KS']     
     }



cases['20190528_KTWX'] = {'date':'20190528',
     'rda':'KTWX',
     'lonmin':-96.26,
     'lonmax':-95.17,
     'latmax':39.15,
     'latmin':38.29,
     'start_latlon': (38.845,-95.383),
     'end_latlon': (38.877,-95.308),
     'start_time': '2019-05-28 23:04:39',
     'end_time': '2019-05-28 23:12:55',
     'storm_motion': (240,31),
     'feature_follow': True,
     'cutlist': ['00.50','00.90'],
     #'cutlist': ['00.50','00.90','01.30','01.80','02.40'],
     'shapelist':['KS','MO','20190528_survey']
     }


cases['20190601_KGRR'] = {'date':'20190601',
     'rda':'KGRR',
     'lonmin':-85.61,
     'lonmax':-84.90,
     'latmax':42.62,
     'latmin':42.06,
     #'extent': [-85.61,-84.90,42.06,42.62],
     'extent': [-86.0,-83.5,41.00,42.0],
     'sat_extent' : [-86.5,-83.2,41.3,43.8],
     'pandas' : ('2019-06-01 23:28', 20, '1min'),
     'eventloc': (-85,19,42.31),
     #'eventloc2': (-94.93,39.06),
     'cutlist': ['00.50'],
     'shapelist':['MI','IN']
     }

cases['20190608_KMVX'] = {'date':'20190608',
     'rda':'KMVX',
     'latmax':47.75,
     'latmin':47.20,
     'lonmin':-97.0,
     'lonmax':-96.3,
     'eventloc': (-96.2146,47.4998),
     'eventloc2': (-96.1488,47.5248),
     'start_latlon': (47.445,-96.3423),
     'end_latlon': (47.50,-96.208),
     'start_time': '2019-06-09 00:23:53',
     'end_time': '2019-06-09 00:37:36',
     'storm_motion': (232,28),  
     'feature_follow': True,
     #'cutlist': ['00.50','00.90','01.30','01.80','02.40'],
     'cutlist': ['02.40','03.10','04.00'],
     'shapelist':['MN','ND']
     }

cases['20190702_KGRR'] = {'date':'20190702',
     'rda':'KGRR',
     'lonmin':-87.0,
     'lonmax':-84.6,
     'latmax':43.9,
     'latmin':42.0,
     'sat_extent' : [-88.0,-85.0,42.3,44.7],
     'pandas' : ('2019-07-02 21:40', 29, '5min'),
     'start_latlon': (43.164,-86.895),
     'end_latlon': (43.08,-86.147),
     'start_time': '2019-07-02 21:40:04',
     'end_time': '2019-07-02 22:28:54',
     'feature_follow': True,
     'cutlist': ['00.50','00.90','01.30','01.80'],
     'storm_motion': (279,39),
     'shapelist':['Lake_MI_counties']
     }

cases['20190704_KGRR'] = {'date':'20190704',
     'rda':'KGRR',
     'lonmin':-86.25,
     'lonmax':-84.75,
     'latmax':43.25,
     'latmin':42.0,
     'sat_extent' : [-86.25,-84.75,42.0,43.25],
     'pandas' : ('2019-07-04 20:15', 24, '5min'),
     'start_latlon': (43.164,-86.895),
     'end_latlon': (43.08,-86.147),
     'start_time': '2019-07-02 21:40:04',
     'end_time': '2019-07-02 22:28:54',
     'feature_follow': False,
     'cutlist': ['00.50','00.90','01.30','01.80'],
     'storm_motion': (279,39),
     'shapelist':['Lake_MI_counties']
     }


cases['20190911_KGRR'] = {'date':'20190911',
     'rda':'KGRR',
     'lonmin':-86.65,
     'lonmax':-85.95,
     'latmax':43.30,
     'latmin':42.75,
     'sat_extent' : [-87.25,-84.75,42.0,44.0],
     'start_latlon': (42.979,-85.722),
     'end_latlon': (42.917,-85.30),
     'start_time': '2019-09-11 23:40:23',
     'end_time': '2019-09-12 00:06:54',
     'pandas' : ('2019-09-11 23:15', 18, '5min'),
     'feature_follow': True,
     'cutlist': ['00.50'],
     'storm_motion': (278,46),
     'start_figures': 20190911231000,     
     'end_figures': 20190912014000,
     'shapelist':['Lake_MI_counties','20190911_survey']
     }

cases['20190720_KGRB'] = {'date':'20190720',
     'rda':'KGRB',
     'lonmin':-92.5,
     'lonmax':-89.45,
     'latmax':46.65,
     'latmin':44.25,
     'sat_extent' : [-86.25,-84.75,42.0,43.25],
     'pandas' : ('2019-07-04 20:15', 24, '5min'),
     'start_latlon': (45.685,-90.444),
     'end_latlon': (45.310,-89.325),
     'start_time': '2019-07-20 00:05:18',
     'end_time': '2019-07-20 01:08:30',
     'feature_follow': True,
     'cutlist': ['00.50','00.90','01.30','01.80'],
     'storm_motion': (305,50),
     'shapelist':['Lake_MI_counties','20190720_paths','20190720_points']
     }

cases['20190720_KGRBB'] = {'date':'20190720',
     'rda':'KGRB2',
     'lonmin':-91.25,
     'lonmax':-89.6,
     'latmax':45.05,
     'latmin':43.75,
     'sat_extent' : [-86.25,-84.75,42.0,43.25],
     'pandas' : ('2019-07-04 20:15', 24, '5min'),
     'start_latlon': (44.40,-90.142),
     'end_latlon': (44.25,-88.325),
     'start_time': '2019-09-11 23:00:00',
     'end_time': '2019-09-12 01:00:00',
     'feature_follow': True,
     'cutlist': ['00.50','00.90','01.30','01.80'],
     'storm_motion': (277,55),
     'shapelist':['Lake_MI_counties','20190720_paths','20190720_points']
     }			

#this_case = cases['eek']
#this_case = cases['20190720_KGRBB']
this_case = cases['20190911_KGRR']
this_case['products'] = ['AzShear_Storm','DivShear_Storm','ReflectivityQC','Velocity','SpectrumWidth', 'RhoHV']
#this_case['cutlist'] =  ['00.90','01.30','01.80']