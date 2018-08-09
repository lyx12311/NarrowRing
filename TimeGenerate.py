#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Author: Lucy Lu (last update 08/03/2018)
# Contain functions: 
#	TimeGenerate(t,printdes,length) [generate a time string for plotting]
#		t: one float/double time (t)
#		printdes: how many desimals to print out 
#		length: how long the integer part is
#
#			example:TimeGenerate(0,2,3)=  0.00
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
import matplotlib.cm as cm
import random
from scipy.interpolate import interp1d

# this function takes into a float/double time, how many desimals to print out and how long the integer part is. It ouputs a string that has proper form for plotting
def TimeGenerate(t,printdes,length):
	timeparts=str(t)
	#print timeparts
	timeprint=[]
	k=0
	for i in range(len(timeparts)+int(printdes)):
		if timeparts[i]=='.':
			timeprint.append(timeparts[i])
			k+=1
		else:
			if k==1:
				if printdes > len(timeparts)-i:
					timeparts=timeparts+'0'*printdes
					#print timeparts
				while k < printdes+1:
					#print(timeparts[i])
					timeprint.append(timeparts[i])
					k+=1
					i+=1
				break
			else:
				timeprint.append(timeparts[i])
				
	#print timeprint	
	timeprint=''.join(map(str, timeprint))	
	return int(length-len(timeprint))*" "+ timeprint
