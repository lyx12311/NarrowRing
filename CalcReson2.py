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
import matplotlib.cm as cm
import random
from scipy.interpolate import interp1d
from hnread import *
from center_angle import *

def checkinput(argv):                                                                       
    programname = sys.argv[0]                                                               
    if len(argv) != 4:  # Exit if not exactly one arguments  
        print '---------------------------------------------------------------------------'                               
        print "This program calculates the resonances between two distances for resonaces smaller than 20, it takes into three arguments:\n Argument 1: Distance of the ring in planet radii\n Argument 2/3: starting/ending position"
        print ' '
        print ' Example:    '+programname+' 2.001 2.23 2.25'  
        print '---------------------------------------------------------------------------'                                    
        sys.exit(1)                                                                                                                                                                                                            
    if float(argv[1])<0 or float(argv[2])<0 or float(argv[3])<0:  # Exit if folder does not exist                  
        print 'ERROR: Distances must be positive '                             
        sys.exit(1)   

checkinput(sys.argv)

def calcR(f,b,dis):
	return (float(b)/float(f))**(2./3.)*dis

Rdis=float(sys.argv[1])

Dis_i=min([float(i) for i in [sys.argv[2],sys.argv[3]]])
Dis_f=max([float(i) for i in [sys.argv[2],sys.argv[3]]])

Ref = [float(j) for j in [i+1 for i in range(20)]]
Reb = [float(j) for j in [i+1 for i in range(20)]]

Dis=[]	
DisS=[]
Resonance=[]
OrderR=[]
#print Dis_i
#print Dis_f

for f in Ref:
	for b in Reb:
		if f==b:
			continue
		else:
			DisU=calcR(f,b,Rdis)
			if DisU>Dis_i and DisU<Dis_f:
				Resonance.append(str(int(b))+":"+str(int(f)))
				OrderR.append(abs(int(b)-int(f)))
				Dis.append(DisU)
				DisS.append(DisU-0.02)
#			Resonance.append(str(int(b))+":"+str(int(f)))
#			Dis.append(DisU)
#			DisS.append(DisU-0.02)

if len(Dis)==0:
	print "No resonances found!"
else:
	Dis,DisS,Resonance,OrderR=zip(*sorted(zip(Dis,DisS,Resonance,OrderR)))
	print "--distance ------- Resonance ------- Order ----"
	for i in range(len(Dis)):
		print str(Dis[i])+"      "+Resonance[i]+"      "+str(OrderR[i])


		

#if len(Ref)==1 and len(Reb)==1:
#	print str(Ref)+":"+str(Reb)+" "+str(calcR(Ref,Reb,Rdis))

