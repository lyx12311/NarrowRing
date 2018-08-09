#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Author: Lucy Lu (last update 08/09/2018)
# Contain functions: 
#	geta(check,Out), gete(check,Out) till getw(check,Out) calculates the element based on input
#	getM(check,Out) till getlatT(check,Out) calculates the element based on input and functions in the previous line
#		check: 1 x 27 array that stores if the element is initially in the file (1) or not (0)
#			example: [1,0,0....,0] means input from the file only contains the time element
#		Out: particle number x 27 matrix that stores all the data for the existing initial condition from file
#
#	getEle(filename,elementout) [returns the element if the element can be calculated/read from the file]
#		filename: file name
#		elementout: element name (e.g. "t", "a", "e", etc...)
#		
#			example: getEle('state1.dat','a') returns data for semimajor axis if exist, if doesn't exist, will return an array with all 0's
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
from hnread import *
from convert_anomalies import *
from chkEle import *

def geta(check,Out):
	if check[14]+check[8]==2:
		return Out[:,14]/(1.-Out[:,8])
	else:
		return 0

def gete(check,Out):
	if check[14]+check[7]==2:
		return 1.-Out[:,14]/Out[:,7]

def getq(check,Out):
	if check[7]+check[8]==2:
		return Out[:,7]*(1.-Out[:,8])
	else:
		return 0

def getW(check,Out):
	# W=cw-w
	if check[11]+check[12]==2:
		return Out[:,12]-Out[:,11]
	# W=lonM-latM
	elif check[17]+check[19]==2:
		return Out[:,17]-Out[:,19]
	# W=lonT-latT
	elif check[18]+check[20]==2:
		return Out[:,18]-Out[:,20]
	# if we have M ... very complicated...
	#elif checkarray[15]==1:
	else:
		return 0

def getw(check,Out):
	# w=cw-W
	if check[10]+check[12]==2:
		return Out[:,12]-Out[:,10]
	# w=latM-M
	elif check[19]==1:
		if check[15]==1:
			return Out[:,19]-Out[:,15]
		elif check[16]+check[8]==2:
			return Out[:,19]- np.array([v2M(Out[i,16],Out[i,8]) for i in range(len(Out[:,16]))])
	# w=latT-T
	elif check[20]==1:
		if check[16]==1:
			return Out[:,20]-Out[:,16]
		elif check[15]+check[8]==2:
			return Out[:,20]- np.array([M2v(Out[i,15],Out[i,8]) for i in range(len(Out[:,15]))])
	else:
		return 0
				
def getcw(check,Out):
	# cw=W+w
	if check[10]+check[11]==2:
		return Out[:,10]+Out[:,11]
	elif check[10]==1 and len(getw(check,Out))!=1:
		return Out[:,10]+getw(check,Out)
	else:
		return 0
		
def getM(check,Out):
	# from nu
	if check[16]+check[8]==2:
		return np.array([v2M(Out[i,16],Out[i,8]) for i in range(len(Out[:,16]))])
	# from M=latM-w
	elif check[19]+check[11]==2:
		return Out[:,19]-Out[:,11]
	elif check[19]==1 and len(getw(check,Out))!=1:
		return  Out[:,19]-getw(check,Out)
	else:
		return 0
		
def getnu(check,Out):
	# from nu
	if check[15]+check[8]==2:
		return np.array([M2v(Out[i,16],Out[i,8]) for i in range(len(Out[:,15]))])
	# from nu=latT-w
	elif check[20]+check[11]==2:
		return Out[:,20]-Out[:,11]
	elif check[20]==1 and len(getw(check,Out))!=1:
		return  Out[:,20]-getw(check,Out)
	else:
		return 0	

def getlonM(check,Out):
	if check[10]+check[11]+check[15]==3:
		return Out[:,10]+Out[:,11]+Out[:,15]
	elif check[10]+check[11]==2 and len(getM(check,Out))!=1:
		return Out[:,10]+Out[:,11]+getM(check,Out)
	elif check[10]+check[15]==2 and len(getw(check,Out))!=1:
		return Out[:,10]+getw(check,Out)+Out[:,15]
	elif check[11]+check[15]==2 and len(getW(check,Out))!=1:
		return getW(check,Out)+Out[:,11]+Out[:,15]
	elif check[11]==1 and len(getM(check,Out))!=1 and len(getW(check,Out))!=1:
		return Out[:,11]+getM(check,Out)+getW(check,Out)
	elif check[10]==1 and len(getM(check,Out))!=1 and len(getw(check,Out))!=1:
		return Out[:,10]+getM(check,Out)+getw(check,Out)
	elif check[15]==1 and len(getW(check,Out))!=1 and len(getw(check,Out))!=1:
		return Out[:,15]+getW(check,Out)+getw(check,Out)
	elif len(getM(check,Out))!=1 and len(getW(check,Out))!=1 and len(getw(check,Out))!=1:
		return getM(check,Out)+getW(check,Out)+getw(check,Out)
	else:
		return 0

def getlonT(check,Out):
	if check[10]+check[11]+check[16]==3:
		return Out[:,10]+Out[:,11]+Out[:,16]
	elif check[10]+check[11]==2 and len(getnu(check,Out))!=1:
		return Out[:,10]+Out[:,11]+getnu(check,Out)
	elif check[10]+check[16]==2 and len(getw(check,Out))!=1:
		return Out[:,10]+getw(check,Out)+Out[:,16]
	elif check[11]+check[16]==2 and len(getW(check,Out))!=1:
		return getW(check,Out)+Out[:,11]+Out[:,16]
	elif check[11]==1 and len(getnu(check,Out))!=1 and len(getW(check,Out))!=1:
		return Out[:,11]+getnu(check,Out)+getW(check,Out)
	elif check[10]==1 and len(getnu(check,Out))!=1 and len(getw(check,Out))!=1:
		return Out[:,10]+getnu(check,Out)+getw(check,Out)
	elif check[16]==1 and len(getW(check,Out))!=1 and len(getw(check,Out))!=1:
		return Out[:,16]+getW(check,Out)+getw(check,Out)
	elif len(getnu(check,Out))!=1 and len(getW(check,Out))!=1 and len(getw(check,Out))!=1:
		return getnu(check,Out)+getW(check,Out)+getw(check,Out)
	else:
		return 0

def getlatM(check,Out):
	if check[11]+check[15]==2:
		return Out[:,11]+Out[:,15]
	elif check[11]==1 and len(getM(check,Out))!=1:
		return Out[:,11]+getM(check,Out)
	elif check[15]==1 and len(getw(check,Out))!=1:
		return Out[:,15]+getw(check,Out)
	elif len(getM(check,Out))!=1 and len(getw(check,Out))!=1:
		return getM(check,Out)+getw(check,Out)
	else:
		return 0

def getlatT(check,Out):
	if check[11]+check[16]==2:
		return Out[:,11]+Out[:,16]
	elif check[11]==1 and len(getnu(check,Out))!=1:
		return Out[:,11]+getnu(check,Out)
	elif check[16]==1 and len(getw(check,Out))!=1:
		return Out[:,16]+getw(check,Out)
	elif len(getnu(check,Out))!=1 and len(getw(check,Out))!=1:
		return getnu(check,Out)+getw(check,Out)
	else:
		return 0

def getEle(filename,elementout):
	data=hnread(filename,"state")
	OutputData=np.zeros((len(data),26))
	headerline=np.array(hnread(filename,"headerline"))
	for i in range(len(headerline)):
		OutputData[:,int(headerline[i])]=data[:,i]
	#print type(OutputData)
	
	
	# get original data
	checkarray=np.zeros(27)
	for i in range(len(checkarray)):
		if str(i) in headerline:
			checkarray[i]=1
			
	# check all the logics
	checklog=chkEle(filename)
	
	# see if it's in original file
	#print [str(geteleInd(elementout))==j for j in headerline]
	if sum([str(geteleInd(elementout))==j for j in headerline])==1:
		return OutputData[:,geteleInd(elementout)]
	
	# if not
	elif chkEle(filename,element=str(elementout))>0:
		if elementout=="a":
			return geta(checkarray,OutputData)
				
		elif elementout=="e":
			return gete(checkarray,OutputData)
				
		elif elementout=="q":
			return getq(checkarray,OutputData)
				
		elif elementout=="W":
			return getW(checkarray,OutputData)
				
		elif elementout=="w":
			return getw(checkarray,OutputData)
				
		elif elementout=="cw":
			return getcw(checkarray,OutputData)
				
		elif elementout=="M":
			return getM(checkarray,OutputData)
		
		elif elementout=="nu":
			return getnu(checkarray,OutputData)
			
		elif elementout=="lonM":
			return getlonM(checkarray,OutputData)
		
		elif elementout=="lonT":
			return getlonT(checkarray,OutputData)
		
		elif elementout=="latM":
			return getlatM(checkarray,OutputData)
		
		elif elementout=="latT":
			return getlatT(checkarray,OutputData)
		
		else:
			print "logic missing, should be able to get"
		
	else:
		print "can't get "+str(elementout)
		return OutputData[:,int(geteleInd(elementout))]

#print getEle("state1.dat","latT")
