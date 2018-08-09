#!/usr/bin/env python
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

def getEle(filename,elementout):
	data=hnread(filename,"state")
	OutputData=np.zeros((len(data),26))
	headerline=np.array(hnread(filename,"headerline"))
	for i in range(len(headerline)):
		OutputData[:,int(headerline[i])]=data[:,i]
	#print type(OutputData)
	
	# check all the logics
	checklog=chkEle(filename)
	
	# see if it's in original file
	if sum([geteleInd(elementout)==j for j in headerline])==1:
		return OutputData[:,geteleInd(elementout)]
	# if not
	elif chkEle(filename,elementout)>0:
		if elementout=="a":
			return OutputData[:,14]/(1.-OutputData[:,8])
		if elementout=="e":
			return 1.-OutputData[:,14]/OutputData[:,7]
		if elementout=="q":
			return OutputData[:,7]*(1.-OutputData[:,8])
		if elementout=="W":

				

getEle("state1.dat","a")
