#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 12:35:19 2024
All counts are in photoelectrons.
@author: janmejoyarch
"""

import numpy as np
from matplotlib import pyplot as plt
from astropy.convolution import convolve, Box2DKernel

def create_circular_mask(h, w, col, row, radius):
    '''
    *** creates circular mask of desired size ***
    - h, w: height and width of canvas
    - col, row: column and row of circle center
    - radius= radius of circle
    '''
    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - col)**2 + (Y-row)**2)
    mask = dist_from_center <= radius
    return mask #can be circular mask of any size

def stripe(power):
    x= np.linspace(0, 20*np.pi, 4096)
    sine_arr= np.ones((4096,4096))
    for i in range(sine_arr.shape[0]):
        y= power*np.sin(x+0.001*i)+1
        sine_arr[i]=sine_arr[i]*y
    return(sine_arr)


shape=(4096,4096)
#Create sun image with 30 pe-. 20 px blur on the edges.
sun= convolve(create_circular_mask(shape[0], shape[1], 2048, 2048, 1420)*3e4, Box2DKernel(20))
shot= np.random.poisson(sun) #introducing random poission noise.
read_noise= np.random.normal(loc= 1500, scale= 8, size= shape) #read noise. Central value (bias) of 1500pe. RMS error of 8e given as STDEV.
image=(shot+read_noise)*stripe(0.01) #sun image with shot noise, bias and read noise, multiplied with pattern.

plt.imshow(image, vmin=0, vmax=3.5e4)
plt.colorbar()
