# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import re

colors = []
steps = []
with open("C:/data/test_curve.txt", "r") as src:
    with open("C:/data/fixed.txt", "w") as dst:
        for line in src:
            data = line.split()
            new_line = '(' + str(data[-3]) + ',' + str(data[-2]) + ',' + str(data[-1]) + ')'
            new_line = '(' + data[-3] + ',' + data[-2] + ',' + data[-1] + ')'
            colors.append(new_line)
            inc = int(data[1])
            final = str((inc + 100)/200.0)
            steps.append(final)

        colors.reverse()
        test1 = 'vel_colors=[' + ','.join(colors) + ']'
        steps.reverse()
        test2 = 'vel_position=[' + ','.join(steps) + ']'    
        print(colors,steps,len(colors),len(steps))
    
        dst.write(test1)
        dst.write('\n')
        dst.write(test2)