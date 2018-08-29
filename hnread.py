#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Author: Lucy Lu (last update 08/03/2018)
# Contain functions: 
#	hnread(filename,typename) [reads files produced by hnbody]
#		filename: file path
#		typename: 
#			"state" (read data into [particle number x element number] matrix)
#			"body" (read data into [particle number x element number] matrix)
#			"headerline" (read headerline number [element number] from state or body file only)
#			"user" (read nearest neightbor)
#			"log" (read cputime)
#			"stream" (read particle number)
#
#			example:hnread("state1.dat","state")=  [particle number x element number] 2D array with data
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
   
d2r = 0.01745329251
r2d = 57.2957795131
# this function reads files produced by hnbody. It reads user.in files, state/body files, log files and stream production files
def hnread(filename,typename):
	#print filename
	if typename == "state":
		headerline = 19
		#print "identify as state file"
		with open(filename) as f:
			parts=f.readlines()
			data=[]
			i=0
			#print len(parts[17:-1])
			for line in parts[headerline:len(parts)]:
				#print line
				linest=line.split()
				#print linest
				data.append([float(j) for j in linest])
				i=i+1
		#print np.array(data)
		return np.array(data)
		
	if typename == "body":
		#print "identify as state file"
		with open(filename) as f:
			parts=f.readlines()
			data=[]
			i=0
			#print len(parts[17:-1])
			for line in parts[17:len(parts)]:
				#print line
				linest=line.split()
				#print linest
				data.append([float(j) for j in linest])
				i=i+1
		#print np.array(data)
		return np.array(data)
	
	if typename == "headerline":
		with open(filename) as f:
			parts=f.readlines()
		return parts[2].split()
		
	# nearest neightbors		
	elif typename == "user":
		with open(filename) as uf:
			parts=uf.readlines()
			NearN=parts[-6].split()
			return float(NearN[-1])
	
	
	elif typename == "log":
		with open(filename) as logf:
			parts=logf.readlines()
			cputime=parts[-2].split()
			return float(cputime[4])
		
		
	elif typename == "stream":
		with open(filename) as stf:
			parts=stf.readlines()
			numbP=parts[5].split()
			return float(numbP[2])
		
		
	else:
		print "typename not recognized!"
		sys.exit(1)


#print hnread("state1.dat","headerline")

