#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Author: Lucy Lu (last update 08/09/2018)
# Contain functions: 
#	chkEle(filename,*positional_parameters,**elementCheck) [check if one/all elements are avaliable to calculate]
#		filename: state/body file that contains a headerline
#		*positional_parameters: 'element'
#		**elementCheck: can be anything from 't' to 'mass' see in function geteleInd for more info
#
#			example: chkEle('state1.dat',element='a') returns 1 (can be caculated/read) or 0 (cannot be calculated/read)
#			example: chkEle('state1.dat') returns 1 x 27 array with 0's (cannot be calculated/read) and 1's (can be caculated/read)
#
#	geteleInd(element) [returns the index of element in hnbody files]
#		element: the element name as a string, read function for more info
#		
#			example: geteleInd('t') returns 0 
#
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
#from hnread import *
#from convert_anomalies import *

def chkEle(filename,*positional_parameters,**elementCheck):
	# get headerlines
	with open(filename) as f:
		parts=f.readlines()
		headerlines=parts[2].split()

	#print headerlines
	#headerlines=np.array(
	
	checkarray=np.zeros(27)
	
	# initial condition
	for i in range(len(checkarray)):
		if str(i) in headerlines:
			checkarray[i]=1

	
	# check if any a,e,q elements can be calculated
	if checkarray[7]+checkarray[8]+checkarray[14] > 1:
		checkarray[7]=1
		checkarray[8]=1
		checkarray[14]=1
		
	# true and mean anomoly 
	if checkarray[15]+checkarray[16] > 0 and checkarray[8]==1:
		checkarray[15]=1
		checkarray[16]=1
	
	# check if any W,cw,w elements can be calculated if all the longtitude and latitude are blank
	if checkarray[17]+checkarray[18]+checkarray[19]+checkarray[20] == 0:
		if checkarray[10]+checkarray[11]+checkarray[12] > 1:
			checkarray[10]=1
			checkarray[11]=1
			checkarray[12]=1
		# check if lat M, lat T can be calculated 
		elif checkarray[11]+checkarray[15]+checkarray[16] > 1:
			checkarray[19]=1
			checkarray[20]=1
	
		# check if longt M, longt T can be calculated
		if checkarray[10]+checkarray[11]+checkarray[12]+checkarray[15]+checkarray[16] > 3:
			checkarray[17]=1
			checkarray[18]=1
		
	# check the other way if we have longt/lat M and/or long/lat T
	
	# latM=w+M
	if checkarray[19]+checkarray[11]+checkarray[15]+checkarray[16] > 1:
		checkarray[19]=1
		checkarray[11]=1
		checkarray[15]=1
		checkarray[16]=1
	
	# latT=w+nu
	if checkarray[20]+checkarray[11]+checkarray[15]+checkarray[16] > 1:
		checkarray[20]=1
		checkarray[11]=1
		checkarray[15]=1
		checkarray[16]=1
	
	# lonM=W+w+M
	if checkarray[17]+checkarray[11]+checkarray[10]+checkarray[15]+checkarray[16] > 2:
		checkarray[17]=1
		checkarray[11]=1
		checkarray[10]=1
		checkarray[15]=1
		checkarray[16]=1
		
	# lonT=W+w+nu	
	if checkarray[18]+checkarray[11]+checkarray[10]+checkarray[15]+checkarray[16] > 2:
		checkarray[18]=1
		checkarray[11]=1
		checkarray[10]=1
		checkarray[15]=1
		checkarray[16]=1

	
	#print checkarray
	if 'element' in elementCheck:
		#print elementCheck['element']
		#print checkarray[geteleInd(elementCheck)]
		return int(checkarray[geteleInd(elementCheck['element'])])
	else:
		return checkarray

	
#chkEle('state1.dat')

def geteleInd(element):
	if element=="t":
		return 0
	elif element=="x":
		return 1
	elif element=="y":
		return 2
	elif element=="z":
		return 3
	elif element=="vx":
		return 4
	elif element=="vy":
		return 5
	elif element=="vz":
		return 6
	elif element=="a":
		return 7
	elif element=="e":
		return 8
	elif element=="i":
		return 9
	elif element=="W" or element=="Omega":
		return 10
	elif element=="w" or element=="omega":
		return 11
	elif element=="cw":
		return 12
	elif element=="T":
		return 13
	elif element=="q":
		return 14
	elif element=="M":
		return 15
	elif element=="nu":
		return 16
	elif element=="lonM":
		return 17
	elif element=="lonT":
		return 18
	elif element=="latM":
		return 19
	elif element=="latT":
		return 20
	elif element=="mass":
		return 21
	else:
		print "Element code not detected!"
		
	
