#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 11:45:53 2025

@author: filippo
"""

#%% Import libraries

import os
import PIL 
import argparse
import numpy as np
import numpy.ma as ma
import imageio.v2 as imageio
import matplotlib.pyplot as plt

from PIL import Image 
from scipy import stats
from index_functions import GLI
import index_functions as indf

#%% read arguments from command line

# Create the parser
parser = argparse.ArgumentParser(description='Calculate vegetation indices from image data')

# Add arguments
parser.add_argument('-b', '--base_folder', type=str, required=True, 
                    help='name of the remote folder of the project')
parser.add_argument('-s', '--target_dir', type=str, required=True, 
                    help='directory where results are to be stored')
parser.add_argument('--fname', type=str, required=True,
                    help='name of image file to be read')
parser.add_argument('--vix', type=str, required=True, default='GLI', 
                    help='name of vegetation index to use')
parser.add_argument('--chan', type=str, required=False, default= 'red,green,blue', 
                    help='List of channels to be used')
# Parse the argument
args = parser.parse_args()

# Print to check arguments values
print('Base folder is:', args.base_folder)
print('Outpunt folder is:', args.target_dir)
print('Name of image file to read is:', args.fname)
print('Name of selected index is:', args.vix)


channels = args.chan.split()
channels = [x.strip() for x in channels]

print(channels)

# %% Reading image file
#base_folder = '/home/filippo/Documents/polyploid_breeding/papers/software_paper/paper-drone2report'
#fname = 'data/single_rgb_plot/single_rgb_plot.tif'
#os.path.join(base_folder, fname)

print("READ THE DATA ...")
fpath = os.path.join(args.base_folder, args.fname)

print("##### Path to image: #####")
print(fpath)
pic = imageio.imread(fpath)

print('Shape of the image : {}'.format(pic.shape))

# %% Masking the corners

print("MASKED ARRAYS ...")
mask_0 = np.all(pic == 0, axis=2)

masked_pixels = np.ma.sum(mask_0)
print("Number of masked pixels is:", masked_pixels)

tot_pixels = mask_0.shape[0] * mask_0.shape[1]

print("Number of available pixels is:", (tot_pixels - masked_pixels))

mask_tot = np.dstack((mask_0,mask_0,mask_0))
masked_pic = ma.masked_array(pic, mask_tot)


# %% calculating the index
print("CALCULATE THE INDEX ...")
print("The selected index is", args.vix)

current_index_function = getattr(indf, args.vix)
print(current_index_function)
# myindex = current_index_function(rb, dataset.get_channels())
                        
                        
ind_vals = current_index_function(masked_pic, channels)

print(ind_vals.shape)

avg_index = round(np.ma.mean(ind_vals),5)
print("Average index value is:", avg_index)

# %% index distribution

print("GET INDEX DISTRIBUTION ...")
print("The selected index is", args.vix)

temp = ind_vals[ind_vals.mask == False]
temp = np.ma.getdata(temp)

print("summary stats on index distribution")
print(stats.describe(temp))

print("quantile distribution of index values")
print(np.quantile(temp, [0.10,0.25,0.5,0.75,0.8,0.9]))

fname = args.vix + '_histogram.png'
fpath = os.path.join(args.base_folder, args.target_dir, fname)

plt.hist(temp, bins=60)
plt.savefig(fpath)

print("Histogram written to ", fpath)

print("END")

