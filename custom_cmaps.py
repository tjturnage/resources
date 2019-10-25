# -*- coding: utf-8 -*-
"""
Creates custom cmaps for matplotlib
https://matplotlib.org/3.1.0/tutorials/colors/colormap-manipulation.html

Assumption: You'll import the created cmaps into wdss_create_netcdfs.py

author: thomas.turnage@noaa.gov
Last updated: 15 Jun 2019

------------------------------------------------

""" 

def make_cmap(colors, position=None, bit=False):
    """
    Creates colormaps (cmaps) for different products.
    
    Information on cmap with matplotlib
    https://matplotlib.org/3.1.0/tutorials/colors/colormap-manipulation.html
    
    Parameters
    ----------
       colors : list of tuples containing RGB values. Tuples must be either:
                - arithmetic (zero to one) - ex. (0.5, 1, 0.75)
                - 8-bit                    - ex. (127,256,192)
     position : ordered list of floats
                None: default, returns cmap with equally spaced colors
                If a list is provided, it must have:
                  - 0 at the beginning and 1 at the end
                  - values in ascending order
                  - a number of elements equal to the number of tuples in colors
          bit : boolean         
                False : default, assumes arithmetic tuple format
                True  : set to this if using 8-bit tuple format
    Returns
    -------
         cmap
                    
    """  
    import numpy as np
    bit_rgb = np.linspace(0,1,256)
    if position == None:
        position = np.linspace(0,1,len(colors))
    else:
        if len(position) != len(colors):
            sys.exit("position length must be the same as colors")
        elif position[0] != 0 or position[-1] != 1:
            sys.exit("position must start with 0 and end with 1")
    if bit:
        for i in range(len(colors)):
            colors[i] = (bit_rgb[colors[i][0]],
                         bit_rgb[colors[i][1]],
                         bit_rgb[colors[i][2]])
    cdict = {'red':[], 'green':[], 'blue':[]}
    for pos, color in zip(position, colors):
        cdict['red'].append((pos, color[0], color[0]))
        cdict['green'].append((pos, color[1], color[1]))
        cdict['blue'].append((pos, color[2], color[2]))

    cmap = mpl.colors.LinearSegmentedColormap('my_colormap',cdict,256)
    return cmap

import matplotlib as mpl
import matplotlib.pyplot as plt
import sys
from metpy.plots import colortables

plts = {}

#-------- Begin creating custom color maps --------

#--- Reflectivity
ref_colors = [(0,0,0),(130,130,130),(95,189,207),(57,201,105),(57,201,105),(0,40,0),(9,94,9),(255,207,0),(255,207,0),(255,207,0),(255,133,0),(255,0,0),(89,0,0),(255,245,255),(225,11,227),(164,0,247),(99,0,214),(5,221,224),(58,103,181),(255,255,255)]
ref_position = [0, 45/110, 46/110, 50/110, 51/110, 65/110, 66/110, 70/110, 71/110, 80/110, 81/110, 90/110, 91/110, 100/110, 101/110, 105/110, 106/110, 107/110, 109/110, 1]
ref_cmap=make_cmap(ref_colors, position=ref_position,bit=True)
plt.register_cmap(cmap=ref_cmap)
plts['ReflectivityQC'] = {'cmap':ref_cmap,'vmn':-30,'vmx':80,'title':'Reflectivity','cbticks':[0,15,30,50,60],'cblabel':'dBZ'}
plts['Ref'] = {'cmap':ref_cmap,'vmn':-30,'vmx':80,'title':'Reflectivity','cbticks':[0,15,30,50,60],'cblabel':'dBZ','title':'Reflectivity'}

#--- Velocity - need to home grow this so I don't require import from metpy
#v_norm, v_cmap = colortables.get_with_range('NWS8bitVel', -40, 40)
#v_cmap.set_under('k')
#plt.register_cmap(cmap=v_cmap)
#vel_colors=[(12,250,250),(221,181,243),(238,186,248),(5,8,255),(14,22,255),(158,238,220),(119,244,154),(146,240,199),(3,239,0),(0,48,0),(87,124,85),(109,131,107),(138,110,124),(132,62,71),(93,2,3),(253,30,46),(253,155,156),(252,202,137),(255,255,0),(238,143,56),(238,143,56),(248,246,245),(248,246,245),(63,18,13),(63,18,13)]
#vel_orig=[0,29,30,59,60,74,75,84,85,109,110,119,120,121,129,130,154,155,164,165,179,180,209,210,240]
#vel_position = []
#for a in vel_orig:
#    vel_position.append(a/240)
#vel_colors=[(0,0,0),(0,155,155),(0,255,235),(144,255,153),(0,255,0),(0,113,0),(83,156,83),(180,180,180),(135,69,88),(119,0,0),(255,0,0),(255,128,0),(255,255,0),(190,190,0),(0,0,0)]
#vel_position = [0, 1/12, 55/240, 65/240, 75/240, 10/24, 11/24, 0.5, 13/24, 14/24, 165/240, 175/240, 185/240, 22/24, 1]
vel_colors=[(0,0,0),(50,65,120),(55,70,130),(75,90,155),(100,120,180),(125,140,200),(175,200,250),(50,115,70),(75,135,90),(105,160,110),(130,180,135),(165,205,160),(225,225,225),(215,190,180),(190,150,130),(160,120,95),(135,85,55),(105,45,10),(240,160,140),(220,120,105),(195,80,70),(165,60,62),(135,55,55),(105,35,45)]
vel_position=[0.0,0.001,0.05,0.1,0.15,0.2,0.25,0.255,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.745,0.75,0.8,0.85,0.9,0.95,1.0]
vel_cmap=make_cmap(vel_colors, position=vel_position,bit=True)
plts['Velocity'] = {'cmap':vel_cmap,'vmn':-100,'vmx':100,'title':'Velocity','cbticks':[-100,-80,-60,-40,-20,0,20,40,60,80,100],'cblabel':'kts'}
plts['Vel'] = {'cmap':vel_cmap,'vmn':-100,'vmx':100,'title':'Velocity','cbticks':[-100,-80,-60,-40,-20,0,20,40,60,80,100],'cblabel':'kts'}
plts['SRV'] = {'cmap':vel_cmap,'vmn':-100,'vmx':100,'title':'SRV','cbticks':[-100,-80,-60,-40,-20,0,20,40,60,80,100],'cblabel':'kts'}
#plts['Velocity'] = {'cmap':vel_cmap,'vmn':-120,'vmx':120,'title':'Velocity','cbticks':[-120,-100,-80,-60,-40,-20,0,20,40,60,80,100,120],'cblabel':'kts'}
#plts['Vel'] = {'cmap':vel_cmap,'vmn':-120,'vmx':120,'title':'Velocity','cbticks':[-120,-100,-80,-60,-40,-20,0,20,40,60,80,100,120],'cblabel':'kts'}
#plts['SRV'] = {'cmap':vel_cmap,'vmn':-120,'vmx':120,'title':'SRV','cbticks':[-120,-100,-80,-60,-40,-20,0,20,40,60,80,100,120],'cblabel':'kts'}

#--- Spectrum Width
sw_colors = [(0,0,0),(220,220,255),(180,180,240),(50,50,150),(255,255,0),(255,150,0),(255,0,0),(255,255,255)]
sw_position = [0, 1/40, 5/40, 0.25, 15/40, 0.5, 0.75, 1]
sw_cmap=make_cmap(sw_colors, position=sw_position,bit=True)
plt.register_cmap(cmap=sw_cmap)
plts['SpectrumWidth'] = {'cmap':sw_cmap,'vmn':0,'vmx':40,'title':'Spectrum Width','cbticks':[0,10,15,20,25,40],'cblabel':'kts'}

#--- CC
#cc_colors = [(145,0,135),(80,0,0),(250,0,0),(255,110,0),(255,210,0),(255,255,0),(130,230,0),(85,255,85),(125,125,255),(0,0,255),(20,20,90),(140,140,140),(50,50,50),(50,50,50),(255,165,255),(255,165,255)]
#cc_colors = [(20,0,50),(30,0,80),(0,0,110),(0,0,170),(0,0,255),(125,125,255),(85,255,85),(130,230,0),(255,255,0),(255,210,0),(255,110,0),(255,0,0),(80,0,0),(25,25,25),(170,170,170),(170,170,170)]
#cc_colors = [(20,0,50),(30,0,80),(0,0,110),(0,0,170),(0,0,255),(125,125,255),(85,255,85),(130,230,0),(255,255,0),(255,210,0),(255,110,0),(255,0,0),(80,0,0),(145,0,135),(255,165,255),(255,165,255)]
#cc_position = [0, 25/84, 35/84, 50/84, 55/84, 60/84, 65/84, 69/84, 70/84, 71.5/84, 74/84, 76/84, 78/84, 80/84, 80.01/84, 1 ]
cc_colors = [(175,175,175),(255,225,200),(100,50,50),(175,150,120),(255,255,75),(35,100,35),(100,255,100),(175,175,175)]
cc_position = [0, 10/105, 50/105, 70/105, 90/105, 96/105, 100/105, 1]
cc_cmap=make_cmap(cc_colors, position=cc_position,bit=True)
plt.register_cmap(cmap=cc_cmap)
plts['RhoHV'] = {'cmap':cc_cmap,'vmn':0.00,'vmx':1.05,'title':'Correlation Coefficient','cbticks':[0.4,0.6,0.8,0.9,1.0],'cblabel':' '}

#--- Velocity Gradient
vg_colors = [(0, 0, 0),(32,32,32),(128,128,128),(117,70,0),(151,70,0),(186,70,0),(220,132,0),(255,153,0),(119,0,0),(153,0,0),(187,0,0),
             (221,0,0),(255,0,0),(255,204,204),(255,204,255),(255,255,255),(255,255,255)]
vg_position = [0, 1/15, 2/15, 3/15, 4/15, 5/15, 6/15, 7/15, 8/15, 9/15, 10/15, 11/15, 12/15, 13/15, 14/15, 0.999999, 1 ]
vg_cmap=make_cmap(vg_colors, position=vg_position,bit=True)
plt.register_cmap(cmap=vg_cmap)
plts['Velocity_Gradient_Storm'] = {'cmap':vg_cmap,'vmn':0.000,'vmx':0.015,'title':'Velocity Gradient','cbticks':[0,0.005,0.010,0.015],'cblabel':'s $\mathregular{^-}{^1}$'}


#--- Azimuthal Shear / Div Shear
azdv_colors = [(1,1,1),(1,1,1),(0,0,1),(0,0,0.7),(0,0,0),(0.7,0,0),(1,0,0),(1,1,1),(1,1,1)]
azdv_position = [0, 0.001, 0.3, 0.43, 0.5, 0.57, 0.7, 0.999, 1]
azdv_cmap=make_cmap(azdv_colors, position=azdv_position)
plt.register_cmap(cmap=azdv_cmap)

#--- Azimuthal Shear / Div Shear Reversed -- 
#--- this makes convergence (i.e., negative divergence) more intuitive to visualize
azdv_colors_r = [(1,1,1),(1,1,1),(1,0,0),(0.7,0,0),(0,0,0),(0,0,0.7),(0,0,1),(1,1,1),(1,1,1)]
azdv_position_r = [0, 0.001, 0.3, 0.43, 0.5, 0.57, 0.7, 0.999, 1]
azdv_cmap_r=make_cmap(azdv_colors_r, position=azdv_position_r)
plt.register_cmap(cmap=azdv_cmap_r)

plts['DivShear_Storm'] = {'cmap':azdv_cmap_r,'vmn':-0.01,'vmx':0.01,'title':'DivShear','cbticks':[-0.010,-0.005,0,0.005,0.010],'cblabel':'s $\mathregular{^-}{^1}$'}
plts['AzShear_Storm'] = {'cmap':azdv_cmap,'vmn':-0.01,'vmx':0.01,'title':'AzShear','cbticks':[-0.010,-0.005,0,0.005,0.010],'cblabel':'s $\mathregular{^-}{^1}$'}

#--------------   Satellite
# got a lot of help from - http://almanydesigns.com/grx/goes/

#--- CH13 (clean IR)
# Using COD version
ir_colors = [(0,0,0),(255,255,255),(0,0,0), (255,0,0), (255,255,0), (0,255,0), (0,0,255), (191,0,255), (255,255,255),(0,0,0),(120,120,120),(0,0,0)]
ir_position = [0, 10/166, 35/166, 45/166, 55/166, 65/166, 82/166, 90/166, 95/166, 135.9/166, 136/166, 1]
ir_cmap=make_cmap(ir_colors, position=ir_position,bit=True)
plt.register_cmap(cmap=ir_cmap)
plts['C13'] = {'cmap':ir_cmap,'vmn':-110.0,'vmx':56.0,'title':'Channel 13 IR'}

#--- W/V CH08,09,10
wv_colors = [(0,255,255),(0,110,0),(255,255,255),(0,0,165),(255,255,0),(255,0,0),(0, 0, 0)]
wv_position = [0, (109-75)/109,(109-47)/109, (109-30)/109, (109-15.5)/109,108/109,1 ]
wv_cmap=make_cmap(wv_colors, position=wv_position,bit=True)
plt.register_cmap(cmap=wv_cmap)
plts['C08'] = {'cmap':wv_cmap,'vmn':-109.0,'vmx':0.0,'title':'Channel 8 W/V'}
plts['C09'] = {'cmap':wv_cmap,'vmn':-109.0,'vmx':0.0,'title':'Channel 9 W/V'}
plts['C10'] = {'cmap':wv_cmap,'vmn':-109.0,'vmx':0.0,'title':'Channel 10 W/V'}


#--- Lightning
ltg_colors = [(4/5,0,0),(0,4/5,0),(0,0,4/5)]
ltg_position = [0,0.6,1]
ltg_cmap=make_cmap(ltg_colors, position=ltg_position)
plt.register_cmap(cmap=ltg_cmap)

#-------- End creating custom color maps --------


#plts['C02'] = {'cmap':'Greys_r','vmn':0.0,'vmx':1.0,'title':'Channel 2 Visible'}
plts['C02i'] = {'cmap':'Greys_r','vmn':0.0,'vmx':1.0,'title':'Channel 2 Visible'}
plts['C02'] = {'cmap':'Greys_r','vmn':0.0,'vmx':1.0,'title':'Channel 2 Visible'}
plts['C03'] = {'cmap':'Greys_r','vmn':0.0,'vmx':1.0,'title':'Channel 3 Near IR'}


plts['GLM'] = {'title':'GLM'}
plts['ltg_low'] = {'title':'Low Lightning'}
plts['ltg_high'] = {'title':'High Lightning'}
