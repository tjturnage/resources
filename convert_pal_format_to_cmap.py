# -*- coding: utf-8 -*-
"""
Takes .pal colortables used in GR2Analyst and creates

       colors : list of tuples containing RGB values. Tuples are:
                - 8-bit ... ex. (127,256,192)
        steps : ordered list of floats
                It must have:
                  - 0 at the beginning and 1 at the end
                  - values in ascending order
                  - a number of elements equal to the number of tuples in colors


Looking for this syntax in the .pal file. In this case values (second column)
are descending, but ascending can be handled too

color:   1.05   175  175  175
color:   1.00   100  255  100   175  175  175
color:   0.96    35  100   35    75  225   75
color:   0.90   255  255   75    35  100   35
color:   0.70   175  150  120   250  250  100
Color:   0.50   100   50   50   175  150  120
color:   0.10   255  225  200   100   50   50
color:   0.00   175  175  175   175  175  175

"""

def normalize(value,offset,value_range):
    normalized = str((value + offset)/value_range)
    return normalized[0:6]

import os
import re

colors = []
steps = []
rgbs = []

p = re.compile('olor:')

gr2_dir = 'C:/Users/thomas.turnage/GR2/ColorCurves'
pal = 'DKC_reflectivity_Snow.pal'
pal_file = os.path.join(gr2_dir,pal)

#create an "rgbs" list with values and color tuple(s)
with open(pal_file, "r") as src:
    with open("C:/data/fixed.txt", "w") as dst:
        for line in src:
            m = p.search(line)
            if m is not None:
                data = line.split()
            #first_element = str(data[0])
            #if first_element == 'Color:' or first_element == 'color:':
                inc = float(data[1])
                if len(data) == 5:
                    tuple1 = '(' + data[-3] + ',' + data[-2] + ',' + data[-1] + ')'
                    thisone = [inc,tuple1]
                elif len(data) == 8:
                    tuple1 = '(' + data[-6] + ',' + data[-5] + ',' + data[-4] + ')'
                    tuple2 = '(' + data[-3] + ',' + data[-2] + ',' + data[-1] + ')'                    
                    thisone = [inc,tuple1,tuple2]

                rgbs.append(thisone)

        # With the created rgbs list, check if the first element value exceeds 
        # the last value. If so, we have descending order
        # take min and max values to calculate data range
        # determine if range crosses zero in which case values will have to be 
        # shifted to keep them all >= 0
        if float(rgbs[0][0]) > float(rgbs[-1][0]):
            descending = True
            min_value = float(rgbs[-1][0])
            max_value = float(rgbs[0][0])
        else:
            descending = False
            min_value = float(rgbs[0][0])
            max_value = float(rgbs[-1][0])

        value_range = max_value - min_value

        if min_value != 0:
            offset = -min_value
        else:
            offset = 0

        # easier to work with a list with increasing values        
        if descending:
            rgbs.reverse()

        # Step through elements in rgbs. Thise with two tuples (len>2), need a new step value
        # for the second rgb tuple that stays just less than the step value of the first tuple 
        # in next element
        #
        # the normalize function takes the original values, accounts for if the range crosses zero
        # then normalizes to the appropriate relative value between 0 and 1.
        #
        # If the rgbs element contains only one color tuple (len=2), then it's a simple append
        for r in range(0,len(rgbs)-1):
            if len(rgbs[r]) > 2:
                inc1 = float(rgbs[r][0])
                inc2 = float(rgbs[r+1][0])
                factor = 0.95*(inc2 - inc1)               
                new_inc = inc1 + factor
                inc_a = normalize(inc1,offset,value_range)
                inc_new = normalize(new_inc,offset,value_range)                    
                inc_c = normalize(inc2,offset,value_range)
                rgb1 = rgbs[r][1]
                rgb2 = rgbs[r][2]
                steps.append(inc_a)
                steps.append(inc_new)
                colors.append(rgb1)
                colors.append(rgb2)
            else:
                orig_step = float(rgbs[r][0])
                inc = normalize(orig_step,offset,value_range)
                rgb1 = rgbs[r][1]
                colors.append(rgb1)
                steps.append(inc)

        # ensures the array ends with 1.0 using the last color tuple
        steps.append('1.0')
        colors.append(rgbs[-1][-1])
        # inserts black (0,0,0) at the very beginning since netcdfs missing data are
        # -9999 and will be assigned the color at the bottom of the curve
        steps.insert(0,'0.0')
        colors.insert(0,'(0,0,0)')
        steps[1] = '0.001'

        test1 = 'colors=[' + ','.join(colors) + ']'
        test2 = 'position=[' + ','.join(steps) + ']'
        print(test1,test2)
        print(len(steps),len(colors))    
        dst.write(test1)
        dst.write('\n')
        dst.write(test2)