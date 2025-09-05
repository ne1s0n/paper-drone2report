#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 12:54:54 2025

@author: filippo
"""

import numpy as np

########
### RGB
########
def HUE(img, channels):
	"""Hue, uses red, green, blue"""
	try:
		red   = img[:,:,channels.index('red')]
		green = img[:,:,channels.index('green')]
		blue  = img[:,:,channels.index('blue')]
	except ValueError:
		#if this clause is activated it means that the requested channel(s) are not available
		return np.nan
	#if we get here the index can be applied to the current image
	return(np.arctan(
		(2*red - green - blue) * (green - blue) / 30.5
	)) 
    

def GLI(img, channels):
	"""Green leaf index, uses red, green, blue"""
	try:
		red   = img[:,:,channels.index('red')]
		green = img[:,:,channels.index('green')]
		blue  = img[:,:,channels.index('blue')]
	except ValueError:
		#if this clause is activated it means that the requested channel(s) are not available
		return np.nan
	#if we get here the index can be applied to the current image
	return(
		(2.0*green - red - blue) / 
		(2.0*green + red + blue)
	) 

def Intensity(img, channels):
	"""Pixel intensity across RGB channels"""
	try:
		red   = img[:,:,channels.index('red')]
		green = img[:,:,channels.index('green')]
		blue  = img[:,:,channels.index('blue')]
	except ValueError:
		#if this clause is activated it means that the requested channel(s) are not available
		return np.nan
	#if we get here the index can be applied to the current image
	return(

        (1 / 30.5) * (red + blue + green)
	) 
    

def NGRDI(img, channels):
	"""Normalized Difference Green/Red Normalized green red difference index, Visible Atmospherically Resistant Indices Green (VIgreen), uses green, red"""
	try:
		red   = img[:,:,channels.index('red')]
		green = img[:,:,channels.index('green')]
	except ValueError:
		#if this clause is activated it means that the requested channel(s) are not available
		return np.nan
	#if we get here the index can be applied to the current image
	return(
		(green - red) / 
		(green + red)
	) 


def ShapeIndex(img, channels):
	"""Shape Index"""
	try:
		red   = img[:,:,channels.index('red')]
		green = img[:,:,channels.index('green')]
		blue  = img[:,:,channels.index('blue')]
	except ValueError:
		#if this clause is activated it means that the requested channel(s) are not available
		return np.nan
	#if we get here the index can be applied to the current image
	return(
		(2*red - green - blue) / 
		(green - blue)
	)


def VARIrgb(img, channels):
    """Visible Atmospherically Resistant Index, uses red, green, blue"""
    try:
        red   = img[:,:,channels.index('red')]
        green = img[:,:,channels.index('green')]
        blue  = img[:,:,channels.index('blue')]
    except ValueError:
        #if this clause is activated it means that the requested channel(s) are not available
        return np.nan
    #if we get here the index can be applied to the current image
    return(
        (green - red) /
        (green + red - blue)
    )


###################
### MULTISPECTRAL 
###################
def NDVI(img, channels):
	"""Normalized vegetation index, uses red, NIR"""
	try:
		red = img[:,:,channels.index('red')]
		NIR = img[:,:,channels.index('nir')]
	except ValueError:
		#if this clause is activated it means that the requested channel(s) are not available
		return np.nan
	#if we get here the index can be applied to the current image
	return(
		(NIR - red) /
		(NIR + red)
	) 

def VARIgreen(img, channels):
	"""Visible Atmospherically Resistant Index Green, uses 459:490, 545:565, 620:680"""
	try:
		w459 = img[:,:,channels.index('459:490')]
		w545 = img[:,:,channels.index('545:565')]
		w620 = img[:,:,channels.index('620:680')]
	except ValueError:
		#if this clause is activated it means that the requested channel(s) are not available
		return np.nan
	#if we get here the index can be applied to the current image
	return(
		(w545 - w620) / 
		(w545 + w620 - w459)
	) 
    
