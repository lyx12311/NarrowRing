#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Author: Lucy Lu (last update 08/03/2018)
# Contain functions: 
#	calc_r(a,e,nu) [calculate radius]
#	calc_dr(a,e,nu,a_r,e_r) [calculate radius difference respect to reference elipse with a_r as a and e_r as e]
#	calc_z(a,e,i,w,nu,omega) [calculate z]
#	centeranle(x,minc,maxc) [Rescale the input argument to a min and a max]
# 		example: center_angle(-10,0,360) = 350
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

import numpy as np
import math
import os
import matplotlib.pyplot as plt
import sys 
import glob
from math import log10, floor
from decimal import *

d2r = 0.01745329251
r2d = 57.2957795131
plotRange=0.5 # the range seeing
printdes=4 # print out time desimals
def calc_r(a,e,nu):
	return a*(1.-e*e)/(1.+e*np.cos(nu*d2r))

def calc_dr(a,e,nu,a_r,e_r):
	return a*(1.-e*e)/(1.+e*np.cos(nu*d2r))-a_r*(1.-e_r*e_r)/(1.+e_r*np.cos(nu*d2r))
	
def calc_z(a,e,i,w,nu,omega):
	return a*(1.-e*e)/(1.+e*np.cos(nu*d2r))*np.sin(i*d2r)*np.sin((w-omega+nu)*d2r)
		
def center_angle(x,minc,maxc): 
	if x >= minc and x <= maxc:
		remain = x
	else:
		rangex = float(maxc)-float(minc)
		if x < minc:
			remain = x + abs(math.ceil((minc-x)/rangex)*rangex)
		elif x > maxc:
			remain = x - abs(math.ceil((x-maxc)/rangex)*rangex)
	return remain
