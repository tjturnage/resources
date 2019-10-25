# -*- coding: utf-8 -*-
"""
Looking for this format
color:   1.05   175  175  175
color:   1.00   100  255  100   175  175  175
color:   0.96    35  100   35    75  225   75
color:   0.90   255  255   75    35  100   35
color:   0.70   175  150  120   250  250  100
Color:   0.50   100   50   50   175  150  120
color:   0.10   255  225  200   100   50   50
color:   0.00   175  175  175   175  175  175
"""


import os
lowest_value = -100.0
highest_value = 100.0

value_range = highest_value - lowest_value

if lowest_value < 0.0:
    neg_offset = -lowest_value
else:
    neg_offset = lowest_value

colors = []
steps = []
gr2_dir = 'C:/Users/thomas.turnage/GR2/ColorCurves'
pal = 'DKC_CC_only.pal'
pal_file = os.path.join(gr2_dir,pal)
with open(pal_file, "r") as src:
    with open("C:/data/fixed.txt", "w") as dst:
        for line in src:
            data = line.split()
            first_element = str(data[0])
            if first_element == 'Color:' or first_element == 'color:':
                if len(data) == 5:
                    new_line = '(' + data[-3] + ',' + data[-2] + ',' + data[-1] + ')'
                    colors.append(new_line)
                    inc = float(data[1])
                    final = str((inc + neg_offset)/value_range)
                    steps.append(final[0:5])
                elif len(data) == 8:
                    tuple1 = '(' + data[-3] + ',' + data[-2] + ',' + data[-1] + ')'
                    colors.append(tuple1)
                    tuple2 = '(' + data[-6] + ',' + data[-5] + ',' + data[-4] + ')'
                    colors.append(tuple2)
                    inc = float(data[1])
                    final = str((inc + neg_offset)/value_range)       
                    steps.append(final[0:5])
                    steps.append(final[0:5])
        


        colors.append('(0,0,0)')
        colors.reverse()
        test1 = 'colors=[' + ','.join(colors) + ']'

        steps[0] = '1.0'
        for i in range(2,len(steps)-1):
            if steps[i] == steps[i-1]:
                steps[i] = str(float(steps[i-1])-0.001)
            else:
                pass

        if steps[-1] == steps[-2] and colors[-1] == colors[-2]:
            steps[-2] = str(float(steps[-3]) - 0.001)

        steps[-1] = '0.00001'
        steps.append('0.0')
        steps.reverse()

        test2 = 'position=[' + ','.join(steps) + ']'    
        print(test1,test2,len(steps),len(colors))
    
        dst.write(test1)
        dst.write('\n')
        dst.write(test2)