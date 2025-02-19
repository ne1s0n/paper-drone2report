#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 11:45:53 2025

@author: filippo
"""

#%% Import libraries

import os
import argparse
import numpy as np
import numpy.ma as ma
import imageio.v2 as imageio
import matplotlib.pyplot as plt

from index_functions import GLI


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
# Parse the argument
args = parser.parse_args()

# Print to check arguments values
print('Base folder is:', args.base_folder)
print('Outpunt folder is:', args.target_dir)
print('Name of image file to read is:', args.fname)

channels = ['red','green','blue']

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
gli = GLI(masked_pic, channels)

print(gli.shape)

avg_index = round(np.ma.mean(gli),5)
print("Average index value is:", avg_index)

# %% index distribution

print("GET INDEX DISTRIBUTION ...")


