#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Author: Lucy Lu (last update 01/07/2019)
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
#			"input" (read Rp and J2, output Rp,J2)
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
   
def stateread(filename,hl):
	headerline = int(hl)
	#print(headerline)
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
	return np.array(data)

def bodyread(filename,hl):
	headerline = int(hl)
	with open(filename) as f:
		parts=f.readlines()
		data=[]
		i=0
		#print len(parts[17:-1])
		for line in parts[headerline:len(parts)]:
			linest=line.split()
			data.append([float(j) for j in linest])
			i=i+1
	return np.array(data)

# headerline
def headread(filename,hl):
	with open(filename) as f:
		parts=f.readlines()
	return parts[2].split()

#nearest neighbor
def userread(filename,hl):
	with open(filename) as uf:
		parts=uf.readlines()
		NearN=parts[-6].split()
	return float(NearN[-1])

#cputime
def logread(filename,hl):
	with open(filename) as logf:
		parts=logf.readlines()
		cputime=parts[-2].split()
		return float(cputime[4])

# number of particles			
def streamread(filename,hl):
	with open(filename) as stf:
		parts=stf.readlines()
		for lines in parts:
			if "N " in lines:
				numbP_l=lines.split("=")[1].split(" ")
				numbP_l=list(filter(None,numbP_l))
		return float(numbP_l[0])

# Rp and J2
def inputread(filename,hl):
	with open(filename) as inpf:
		parts=inpf.readlines()
		for lines in parts:
			if "LengthUnit" in lines:
				#print(lines.split(":")[1].split(" "))
				Rp=lines.split(":")[1].split(" ")
				Rp=list(filter(None,Rp))[0]
			elif "OblateJ2" in lines:
				J2=lines.split("=")[1].split(" ")
				J2=list(filter(None,J2))[0].split("\n")[0]
		return float(Rp),float(J2)

dic = {"state":stateread,"body":bodyread,"headerline":headread,"user":userread,"log":logread,"stream":streamread,"input":inputread}
		
d2r = 0.01745329251
r2d = 57.2957795131
# this function reads files produced by hnbody. It reads user.in files, state/body files, log files and stream production files
def hnread(filename,typename,hl='17'):
	#print typename
	#return dic[str(typename)](filename)
	try:
		return dic[str(typename)](filename,hl)	
	except:
		print "typename not recognized!" 
		sys.exit(1)


#print hnread("state1.dat","headerline")

