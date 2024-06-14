#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 12:35:19 2024
- Code generated to make synthetic striped pattern and to
check which kernel size is optimized for isolating the
striped structure.
- It is seen that the performance is optimized when the kernel size
is similar to the size of the striped pattern.

- All counts are in photoelectrons.

@author: janmejoyarch
"""

import numpy as np
from astropy.convolution import convolve, Box2DKernel
from concurrent.futures import ProcessPoolExecutor

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

def stripe(power, omega):
    x= np.linspace(0, omega*np.pi, 4096)
    sine_arr= np.ones((4096,4096))
    for i in range(sine_arr.shape[0]):
        y= power*np.sin(x-0.001*i)+1 #Make diagonal stripe pattern
        sine_arr[i]=sine_arr[i]*y
    return(sine_arr)

def blur(data, kernel): #blurring function
    return(convolve(data, Box2DKernel(kernel), normalize_kernel=True))

def dust(base, row, col, size):
    base[row:row+size, col:col+size]= 500
    return(base)

def run(filt_rad):
    large_scale_img= blur(small_scale_removed_img, filt_rad)
    std= np.std(large_scale_img[750:-750, 750:-750])
    mean= np.mean(large_scale_img[750:-750, 750:-750])
    pc_dev= std*100/mean
    print(filt_rad, pc_dev)

if __name__=='__main__':
    freq=13
    stripe_image= stripe(0.01, freq)
    shape=(4096,4096)    
    base= dust(np.full(shape, 6e4), 1000, 1000, 8) #Base illumination with dust spots
    
    #NOISE#
    shot= np.random.poisson(base) #introducing random poission noise in flat illumination.
    prnu= np.random.normal(loc=1, scale=0.1, size=shape) #1% PRNU
    read_noise= np.random.normal(loc= 1500, scale= 8, size= shape) #read noise. Central value (bias) of 1500pe. RMS error of 8e given as STDEV.
    
    #IMG-GENERATION#
    image_pe=(shot*prnu*stripe_image)+read_noise #flat image with shot noise, bias and read noise, multiplied with pattern.
    bias_corrected_image= (image_pe/3)-500 #bias corrected, pe to ADU converted.
    
    #FILTERING#
    small_scale_removed_img= blur(bias_corrected_image, 13) #removes small scale structures (PRNU and CCD dust)
    #large_scale_img= blur(small_scale_removed_img, 200) #isolates large scale illumination changes.
    
    #DIAGNOSTICS#
    filt_rad_list= [30, 50, 100, 300, 500, 550, 600, 610, 620, 630, 640, 650, 700]
    dev_ls= []
    
    print(f"#x= np.linspace(0, {freq}*np.pi, 4096)")
    print("#Filt_rad | % Deviation")
    with ProcessPoolExecutor() as executor:
        executor.map(run, filt_rad_list)
    
    
    
    
    
    