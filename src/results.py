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

data= np.loadtxt('../results/result.txt')
fit= interp1d(data[:,0], data[:,1], kind='quadratic')
x_interp= np.arange(30, 650, 1)
y_interp= fit(x_interp)

print('Min Boxcar Radius', x_interp[np.where(y_interp==np.min(y_interp))])

plt.figure()
plt.plot(data[:,0], data[:,1], '-o')
plt.plot(x_interp, y_interp)
plt.xlabel('Boxcar size')
plt.ylabel('% St Dev')




