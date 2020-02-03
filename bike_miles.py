# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 10:45:09 2020

@author: tjtur
"""

from datetime import datetime

num = 26.7

now = datetime.utcnow()
day_of_year = datetime(now.year,now.month,now.day).timetuple().tm_yday
days_left = 366 - day_of_year
miles_left = 1000 - num

miles_per_day = miles_left / days_left
print(miles_per_day)