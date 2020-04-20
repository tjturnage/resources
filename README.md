# resources
methods, dictionaries, etc. to be shared among different repositories by being imported

case_data.py
------------
Dictionaries of metadata for the various cases to define how radar/satellite graphics
are created.

my_functions.py
---------------
An assortment of functions that aid in processing and plotting netcdf files

hanis_min.js
------------
javascript code that allows one to step through images in a directory
requires a list of image filenames to be created and inserted into the code

gis_layers.py
-------------
dictionaries that reference both counties and storm survey shapefiles
uses cartopy to create shapefile objects

custom_cmaps.py
---------------
creates colormaps (cmaps) to use for plotting in matplotlib
feature a make_cmap function that takes a color list and position list
to build and register the cmaps

convert_pal_format_to_cmap.py
-----------------------------
Creates the needed inputs for the make_cmap function in custom_cmaps.py
Input is a pal file used to defined colortables in GR2Analyst
Output is a fixed.txt file containing the color and position lists required in custom_cmaps.py
