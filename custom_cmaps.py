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
import numpy as np
import matplotlib.pyplot as plt
import sys
#from metpy.plots import colortables

plts = {}
cmaps = {}

#-------- Begin creating custom color maps --------

#--- Reflectivity

colors = [(0,0,0),(130,130,130),(95,189,207),(57,201,105),(57,201,105),(0,40,0),(9,94,9),(255,207,0),(255,207,0),(255,207,0),(255,133,0),(255,0,0),(89,0,0),(255,245,255),(225,11,227),(164,0,247),(99,0,214),(5,221,224),(58,103,181),(255,255,255)]
position = [0, 45/110, 46/110, 50/110, 51/110, 65/110, 66/110, 70/110, 71/110, 80/110, 81/110, 90/110, 91/110, 100/110, 101/110, 105/110, 106/110, 107/110, 109/110, 1]
cmaps['dkc_z'] = {'colors':colors,'position':position, 'min':-30,'max':80}

colors = [(0,0,0),(50,65,120),(55,70,130),(75,90,155),(100,120,180),(125,140,200),(175,200,250),(50,115,70),(75,135,90),(105,160,110),(130,180,135),(165,205,160),(225,225,225),(215,190,180),(190,150,130),(160,120,95),(135,85,55),(105,45,10),(240,160,140),(220,120,105),(195,80,70),(165,60,62),(135,55,55),(105,35,45)]
position=[0.0,0.00001,0.05,0.1,0.15,0.2,0.25,0.255,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.745,0.75,0.8,0.85,0.9,0.95,1.0]
cmaps['dkc_v'] = {'colors':colors,'position':position, 'min':-100,'max':100}


z = cmaps['dkc_z']
v = cmaps['dkc_v']

vel_max = 100
vels_array = np.linspace(-vel_max,vel_max,11)
vticks = np.ndarray.tolist(vels_array)

ref_cmap=make_cmap(z['colors'], position=z['position'],bit=True)
plt.register_cmap(cmap=ref_cmap)
plts['ReflectivityQC'] = {'cmap':ref_cmap,'vmn':z['min'],'vmx':z['max'],'title':'Reflectivity','cbticks':[0,15,30,50,60],'cblabel':'dBZ'}
plts['Ref'] = plts['ReflectivityQC']

vel_cmap=make_cmap(v['colors'], position=v['position'],bit=True)
plt.register_cmap(cmap=vel_cmap)
plts['Velocity'] = {'cmap':vel_cmap,'vmn':v['min'],'vmx':v['max'],'title':'Velocity','cbticks':vticks,'cblabel':'kts'}
plts['Vel'] = plts['Velocity']
plts['SRV'] = plts['Velocity']


#--- Spectrum Width
sw_colors = [(0,0,0),(220,220,255),(180,180,240),(50,50,150),(255,255,0),(255,150,0),(255,0,0),(255,255,255)]
sw_position = [0, 1/40, 5/40, 0.25, 15/40, 0.5, 0.75, 1]
sw_cmap=make_cmap(sw_colors, position=sw_position,bit=True)
plt.register_cmap(cmap=sw_cmap)
plts['SpectrumWidth'] = {'cmap':sw_cmap,'vmn':0,'vmx':40,'title':'Spectrum Width','cbticks':[0,10,15,20,25,40],'cblabel':'kts'}

#--- CC
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
