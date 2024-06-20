#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 00:13:33 2024

Created to validate that the Optimized Boxcar size that can be used
should be as per the frequency of the repetitive pattern.

@author: janmejoyarch
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

filename= '13'#.txt
save=True
data= np.loadtxt(f'../results/{filename}.txt')
fit= interp1d(data[:,0], data[:,1], kind='quadratic')
x_interp= np.arange(30, 700, 0.1)
y_interp= fit(x_interp)
opt_radius= x_interp[np.where(y_interp==np.min(y_interp))][0]
print('Optimal Boxcar Radius', opt_radius, 'px')

plt.figure()
plt.plot(data[:,0], data[:,1], '-o', label='data')
plt.plot(x_interp, y_interp, label='interpolated')
plt.xlabel('Boxcar size')
plt.ylabel('% St Dev')
plt.axvline(opt_radius,ls='--', color='black', label=f'Optimal= {round(opt_radius, 1)} px')
plt.legend()
if save: 
    plt.savefig(f'../results/{filename}.pdf', dpi=300)
    print("Plot Saved in 'results'")




