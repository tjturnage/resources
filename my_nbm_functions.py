# -*- coding: utf-8 -*-
"""


"""

import os
from datetime import datetime,timedelta
import pandas as pd
import matplotlib as plt
import numpy as np
import math
import requests
from reference_data import state2timezone,time_shift_dict

from reference_data import set_basic_paths
data_dir,scripts_dir,image_dir = set_basic_paths()
nbm_script_dir = os.path.join(scripts_dir,'NBM')
nbm_image_dir = os.path.join(image_dir,'NBM')

basic_elements = ['UTC','TMP','TSD','DPT','SKY','WDR','WSP','WSD','GST','GSD',
                  'PZR','PSN','PPL','PRA','VIS']
hourly_elements = ['P01','Q01','T01','S01','I01','CIG','LCB']
short_elements = ['P06','Q06','T06','S06','I06','T03']


qpf_color = (0.1, 0.9, 0.1, 1)
ra_color = (0, 153/255, 0, 1)
sn_color = (0, 153/255, 204/255, 1.0)
zr_color = (204/255,153/255,204/255, 1.0)
pl_color = (240/255,102/255,0,1.0)
pop_color = (0.7, 0.7, 0.7, 1)

prob_yticks = [0, 20, 40, 60, 80, 100]
prob_ytick_labels = ["0","20", "40","60","80","100"]
p_min = -5
p_max = 105

sn_accum_ticks = [0, 1, 2, 4, 8]
sn_accum_tick_labels = ['0', '1', '2', '4', '8']

#         'ymin':p_min,'ymax':p_max,'yticks':prob_yticks,'ytick_labels':prob_ytick_labels, 'title':'Prob Rain\n(%)'}

prods = {}
prods['apraf_bar'] = {'lw': 2, 'zord': 10, 'color': ra_color, 'ymin':p_min, 'ymax':p_max, 'yticks':prob_yticks, 'ytick_labels':prob_ytick_labels, 'bottom':0, 'title':'Prob Rain\n(%)'}
prods['apsnf_bar'] = {'lw': 2, 'zord': 10, 'color': sn_color, 'ymin':p_min, 'ymax':p_max, 'yticks':prob_yticks, 'ytick_labels':prob_ytick_labels, 'bottom':0, 'title':'Prob Snow\n(%)' }
prods['apzrf_bar'] = {'lw': 2, 'zord': 10, 'color': zr_color, 'ymin':p_min, 'ymax':p_max, 'yticks':prob_yticks, 'ytick_labels':prob_ytick_labels, 'bottom':0, 'title':'Prob\nFz Rain(%)'}
prods['applf_bar'] = {'lw': 2, 'zord': 10, 'color': pl_color, 'ymin':p_min, 'ymax':p_max, 'yticks':prob_yticks, 'ytick_labels':prob_ytick_labels, 'bottom':0, 'title':'Prob\nPL(%)'}
prods['aptsf_bar'] = {'lw': 2, 'zord': 10, 'color': pl_color, 'ymin':p_min, 'ymax':p_max, 'yticks':prob_yticks, 'ytick_labels':prob_ytick_labels, 'bottom':0, 'title':'Prob\nTS(%)'}
prods['popf_bar'] = {'lw': 6, 'zord': 9, 'color': pop_color, 'title':'Precip\nChances\n(%)'}
prods['qp_bar'] = {'color':qpf_color, 'ymin':0.0,'ymax':0.50,
                    'yticks':[0.0,0.1,0.2,0.3], 'ytick_labels':['0','0.1','0.2','0.3'],
                    'title':'Precip\nAmount\n(inches)'}    


prods['aptsf_ts'] = {'color':ra_color,
         'ymin':p_min,'ymax':p_max,'yticks':prob_yticks,'ytick_labels':prob_ytick_labels, 'title':'Prob Tstm\n(%)'}

prods['apraf_ts'] = {'color':ra_color,
         'ymin':p_min,'ymax':p_max,'yticks':prob_yticks,'ytick_labels':prob_ytick_labels, 'title':'Prob Rain\n(%)'}

prods['apzrf_ts'] = {'color':zr_color,
         'ymin':p_min,'ymax':p_max,'yticks':prob_yticks,'ytick_labels':prob_ytick_labels, 'title':'Prob Tstm\n(%)'}

prods['apsnf_ts'] = {'color':sn_color,
         'ymin':p_min,'ymax':p_max,'yticks':prob_yticks,'ytick_labels':prob_ytick_labels, 'title':'Prob Snow\n(%)'}

prods['applf_ts'] = {'color':pl_color,
         'ymin':p_min,'ymax':p_max,'yticks':prob_yticks,'ytick_labels':prob_ytick_labels, 'title':'Prob Snow\n(%)'}


prods['popf_ts'] = {'color':(0.7, 0.7, 0.7, 1),
         'ymin':p_min,'ymax':p_max,'yticks':prob_yticks,'ytick_labels':prob_ytick_labels, 'title':'Prob Precip\n(%)'}


prods['apzrf_ts'] = {'color':zr_color,
         'ymin':p_min,'ymax':p_max,'yticks':prob_yticks,'ytick_labels':prob_ytick_labels, 'title':'Prob Ice\n(%)'}

prods['acqp_bar'] = {'color':qpf_color,'ymin':0,'ymax':4.01,'bottom':0,
         'yticks':[0,0.5,1,1.5,2,3],'ytick_labels':['0','0.5','1.0','1.5','2.0','3.0'],    
         'title':'Rain\nAccum\n(in)' }



prods['sn_bar'] = {'color':sn_color,'ymin':0.0,'ymax':1.01,'yticks':[0,0.25,0.5,0.75,1],
     'ytick_labels':['0','1/4','1/2','3/4','1'], 'bottom':0, 'title':'Hourly\nSnow' }

prods['acsn_bar'] = {'color':sn_color,'ymin':0,'ymax':sn_accum_ticks[-1],'bottom':0,
         'yticks':sn_accum_ticks,'ytick_labels':sn_accum_tick_labels, 'bottom':0,    
         'title':'Snow\nAccum\n(in)' }

prods['winter_bar'] = {'color':sn_color,'ymin':0,'ymax':sn_accum_ticks[-1],'bottom':0,
         'yticks':sn_accum_ticks,'ytick_labels':sn_accum_tick_labels, 'bottom':0,    
         'title':'Snow\nAccum\n(in)' }

prods['sn_cat_bar'] = {'color':sn_color,'ymin':0,'ymax':7,'bottom':0,
         'yticks':[0,1,2,3,4,5,6,7],'ytick_labels':['0.0','0.1','0.2','0.5','0.8','1.0','1.5','2.0'],    
         'title':'Snow\nAmount\n(in)' }

    #-------------- Freezing Rain


prods['zr_bar'] = {'color':zr_color,
     'ymin':0.0,'ymax':0.21,'yticks':[0.05, 0.10, 0.15, 0.20],
     'ytick_labels':['0','.05','.10','.15',',20'], 'title':'Hourly\nIce' }

prods['aczr_bar'] = {'color':zr_color,'ymin':0,'ymax':1.01,'bottom':0,
         'yticks':[0,0.1,0.25,0.5,0.75,1],'ytick_labels':['0','0.1','0.25','0.5','0.75','1'],    
         'title':'Ice\nAccum\n(in)' }





prods['wind'] = {'color':(0.5, 0.5, 0.5, 0.8),'ymin':0,'ymax':1,'yticks':[0.27,0.37,0.62],
         'ytick_labels':['Gust (mph)','Speed (mph)','Wind\nDirection'],'title':''}# Wind Speed\nand Gusts\n(mph)'}

prods['t_bar'] = {'color':(255/255, 0, 0, 1.0),'ymin':0,'ymax':80,'bottom':0,
         'yticks':[20,35,52,65],'ytick_labels':['0','15','32','45'],
         'minor_yticks':[60],'minor_yticks_labels':['30']}#,
         #'title':'Temperature\nWind Chill\n(F)' }

prods['wc_bar'] = {'color':(0, 0, 204/255, 1.0),'ymin':0,'ymax':75,'bottom':0,
         'yticks':[30,45,62,75],'ytick_labels':['0','15','32','45'],
         'minor_yticks':[60],'minor_yticks_labels':['30'],
         'title':'Temperature\n(red)\n\nWind Chill\n(blue)'}

prods['ttfb_bar'] = {'color':(0.9, 0.9, 0.2, 1.0),'ymin':0.5,'ymax':4.5,
                        'yticks':[1,2,3,4],'ytick_labels':['under 5','5','15-30','30+'],
                        'title':'Time to\nFrostbite\n(min)'}

prods['sky_bar'] = {'color':(0.6, 0.6, 0.6, 1.0),
         'ymin':-5,'ymax':105,'yticks':[0,25,50,75,100],
         'ytick_labels':['0','25','50','75','100'], 'title':'Sky cover\n(%)'}

prods['vis_cat_bar'] = {'color':(150/255,150/255,245/255, 1.0),
         'ymin':0,'ymax':6,'bottom':0,
         'yticks':[0,1,2,3,4,5,6],'ytick_labels':['0.00','0.25','0.50','1.00','2.00','3.00',' > 6'],    
         'title':'Visibility\n(miles)' }

# conditional probabilities for rain (PRA), snow (PSN), freezing rain (PZR), sleet (PPL)
# define y axis range and yticks/ylabels for any element that's probabilistic 




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
    hr_shift = tz_shift
    fcst_hour_zero_local = fcst_hour_zero_utc - timedelta(hours=hr_shift)

    #pTime = pd.Timestamp(fcst_hour_zero_utc)
    pTime = pd.Timestamp(fcst_hour_zero_local)
    if bulletin_type == 'nbhtx':
        idx = pd.date_range(pTime, periods=27, freq='H')
    else:
        idx = pd.date_range(pTime, periods=23, freq='3H')        
    return idx, fcst_hour_zero_local


def round_values(x,places,direction):
    amount = 10**places
    if direction == 'up':
        return int(math.ceil(x / float(amount))) * int(amount)
    if direction == 'down':
        return int(math.floor(x / float(amount))) * int(amount)


def temperature_bounds(t_shifted_list,wind_chill_shifted_list):
    max_val = np.max(t_shifted_list)
    min_val = np.min(wind_chill_shifted_list)
    high_list = np.arange(100,-40,-10)

    for hi in range(0,(len(high_list))):
        if high_list[hi] > max_val:
            upper_limit = high_list[hi]
        else:
            break
    upper_limit = upper_limit + 10     

    low_list = np.arange(-40,100,10)
    for lo in range(0,(len(low_list))):
        if low_list[lo] < min_val:
            lower_limit = low_list[lo]
        else:
            break
    
    tick_list = np.arange(lower_limit,upper_limit,10)
    tick_labels = []
    for t in range(0,len(tick_list)):
        tick_label = str(int(tick_list[t] - 40))
        tick_labels.append(tick_label)
    print(tick_list,tick_labels)
    return tick_list,tick_labels    


def precip_upper_bounds(x01_accum_list,y_label_list):
    tick_list = []
    tick_label_list = []
    y_label_list_shift = y_label_list[1:]
    print(y_label_list_shift)
    max_val = np.max(x01_accum_list)


    for hi in range(0,(len(y_label_list_shift))):
        this_tick = y_label_list[hi]
        if int(this_tick) < max_val:
            tick_list.append(int(this_tick))
            tick_label_list.append(str(this_tick))
        
    print(tick_list,tick_label_list)
    return tick_list,tick_label_list

    
def u_v_components(wdir, wspd):
    # since the convention is "direction from"
    # we have to multiply by -1
    # If an arrow is drawn, it needs a dx of 2/(number of arrows) to fit in the row of arrows
    u = (math.sin(math.radians(wdir)) * wspd) * -1.0
    v = (math.cos(math.radians(wdir)) * wspd) * -1.0

    return u,v


def myround(x, base=2):

    if x <= 1:
        x = x + 0.25
        1 * round(x/1)
        tick_list = np.arange(0,x,0.25)
        ticks = tick_list
        labels = [str(a) for a in tick_list]
    elif x <= 2:
        x = x + 0.5
        1 * round(x/1)
        tick_list = np.arange(0,x,0.5)
        ticks = tick_list
        labels = [str(a) for a in tick_list]
    elif x <= 4:
        x = x + 1
        2 * round(x/2)
        tick_list = np.arange(0,x,1)
        ticks = [int(a) for a in tick_list]
        labels = [str(a) for a in ticks]
    else:
        x = x + 2
        2 * round(x/2)
        tick_list = np.arange(0,x,2)        
        ticks = [int(a) for a in tick_list]
        labels = [str(a) for a in ticks]

    #print(ticks,labels)
    return ticks,labels
    
def nbm_station_dict(scripts_dir):
    
    fin = os.path.join(scripts_dir,'NBM','NBM_stationtable_20190819.csv')
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


def wind_chill(t,s):
    """
    Returns wind chill in degress F
    Inputs:
        t   : temperatures in degrees F
        s   : wspd in MPH
    """    
    wc = 35.74 + 0.6215*t - 35.75*(s**0.16) + 0.4275*t*(s**0.16)
    #print(round(wc))
    if wc <= t:
        return round(wc)
    else:
        return round(t)

def time_to_frostbite(wc):
    """
    0 to -15        :   >30 minutes
    -15 to -30      :   15 to 30 minutes
    -30 to -50      :   <15 minutes
    <  -50   :   < 5 minutes
    """
    if wc >= -15:
        fbt = 4
    if wc < -15:
        fbt = 3
    if wc < -30:
        fbt = 2
    if wc < -50:
        fbt = 1
                
    return fbt

def define_mosaic_size(products):
    mosaic_size = {}
    mosaic_size[1] = {'h':6,'w':7,'rows':1,'columns':1}
    mosaic_size[2] = {'h':6,'w':15,'rows':1,'columns':2}
    mosaic_size[3] = {'h':6,'w':17,'rows':1,'columns':3}
    mosaic_size[4] = {'h':12,'w':14,'rows':2,'columns':2}
    mosaic_size[6] = {'h':6,'w':10,'rows':2,'columns':3}
    height = mosaic_size[len(products)]['h']
    width = mosaic_size[len(products)]['w']
    rows = mosaic_size[len(products)]['rows']
    cols = mosaic_size[len(products)]['columns']
    return width, height, rows, cols



def categorize(data_list,element):
    """
    Categorizes different weather elements based on
    dictionaries for each element. This is to make plots
    of NBM text bulletins more clear.
    
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




# def synthetic_data():
#     t_list = np.arange(20,-5,-1)
#     t_shifted_list = t_list + 40

#     wspd_list_temp = np.arange(17,29.5,0.5)
#     wspd_arr = np.rint(wspd_list_temp)
#     wspd_list = wspd_arr.astype(int)
#     wdir_list = np.arange(140,43,-4)
#     vis_test = np.arange(10,0.1,-0.4)
#     vis_list = categorize(vis_test,'vis')
#     sn_test = np.arange(0,2.5,0.1)
#     sn_list = categorize(sn_test,'sn')
#     zr_test = np.arange(1,26,1)
#     zr_list = categorize(zr_test,'zr')

#     wind_chill_list = []
#     time_to_fb_list = []
#     for chill in range(0,len(wspd_list)):
#         wc = wind_chill(t_list[chill],wspd_list[chill])
#         time_to_fb = time_to_frostbite(wc)
#         wind_chill_list.append(wc)
#         time_to_fb_list.append(time_to_fb)
#     wind_chill_list = np.asarray(wind_chill_list, dtype=np.float32)
#     wc_cat = categorize(wind_chill_list,'wc')
#     wind_chill_shifted_list = wind_chill_list + 40
#     map_plot_stations[key] = {'lon':lon,'lat':lon,'wc_cat':wc_cat[0]}
#     # Temp (t) and wind chill (wc) go on same panel, 
#     # so using min(wc) and max(t) to define bounds for 'twc'
#     # using a temperature_bounds function
#     twc_tick_list,twc_tick_labels = temperature_bounds(t_shifted_list,wind_chill_shifted_list)
