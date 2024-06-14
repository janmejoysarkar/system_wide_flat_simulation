#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 15:27:38 2024

@author: janmejoyarch
"""

from astropy.io import fits
import matplotlib.pyplot as plt
import os
import numpy as np
from astropy.convolution import Box2DKernel, convolve


def stripe(power):
    x= np.linspace(0, 20*np.pi, 4096)
    sine_arr= np.ones((4096,4096))
    for i in range(sine_arr.shape[0]):
        y= power*np.sin(x-0.001*i)+1 #Make diagonal stripe pattern
        sine_arr[i]=sine_arr[i]*y
    return(sine_arr)

def linear(x, m, c):
    return(m*x+c)

project_path= os.path.expanduser('~/Dropbox/Janmejoy_SUIT_Dropbox/flat_field/system_wide_flat_simulation_project/')
data_path= os.path.join(project_path, 'data/external/lighten_BB03.fits')
data= fits.open(data_path)[0].data
data= convolve(data, Box2DKernel(25))
line_1= data[2000][600:3000]
line_2= data[1700][600:3000]
x= np.arange(len(line_1))

fit1= np.polyfit(x,line_1, 1)
fit2= np.polyfit(x,line_2, 1)

y1, y2= linear(x, fit1[0], fit1[1]), linear(x, fit2[0], fit2[1])

shift=50

plt.figure()
plt.plot(line_1/y1)
plt.plot(x, line_2/y2)
plt.plot(x+shift, line_2/y2)

plt.imshow(data, origin='lower')

print(f'frequency={320 * np.cos(1/6)}')


'''
line_prof= np.sum(data, axis=1)
x= np.arange(len(line_prof))
a,b,c= np.polyfit(x, line_prof, 2)
y= a*x**2+b*x+c
'''