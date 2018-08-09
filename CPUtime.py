#!/usr/bin/env python
##### !/usr/local/bin/python
##### !/usr/bin/python # for DPH mac
import numpy as np
import math
import os
import matplotlib.pyplot as plt
import sys 
import glob
from math import log10, floor
from decimal import *
from scipy.optimize import curve_fit

d2r = 0.01745329251
r2d = 57.2957795131

def funcfit(x,a1,a2,a3):
	return a1*x*x+a2*x+a3
def funclinfit(x,m,b):
	return m*x+b

fig, ax1 = plt.subplots()
NP=[3.,6.,10.,20.,40.,80.,160.,320.,500.,600.,1000.]
CPUtime=[0.03,0.04,0.04,0.06,0.1,0.14,0.34,0.66,1,1.12,1.74]
CPUtimeT=[0.04,0.04,0.05,0.08,0.17,0.45,1.44,5.17,12.11,17.21,46.68]

popt,pcov=curve_fit(funcfit,NP,CPUtimeT)
popt2,pcov2=curve_fit(funclinfit,NP,CPUtime)

ax1.plot(NP,CPUtime,'bo', label="Nearest Neighbor 4")
ax1.hold(True)
ax1.plot(NP,[funclinfit(i,popt2[0],popt2[1]) for i in NP],'b-',label='fit: %5.3f x + %5.3f' % tuple(popt2))
ax1.set_xlabel('Number of Particles')
ax1.set_ylabel('CPU time [s]', color='b')
ax1.tick_params('y', colors='b')
ax1.legend(loc=2)

ax2 = ax1.twinx()
ax2.plot(NP,CPUtimeT,'ro', label="Nearest Neighbor all")
ax2.hold(True)
ax2.plot(NP,[funcfit(i,popt[0],popt[1],popt[2]) for i in NP],'r-',label='fit: %5.3f x^2 + %5.3f x + %5.3f' % tuple(popt))
ax2.set_ylabel('CPU time [s]', color='r')
ax2.tick_params('y', colors='r')
fig.tight_layout()

ax2.legend(loc=4)
#plt.show()
plt.savefig('CPUtime.png')

