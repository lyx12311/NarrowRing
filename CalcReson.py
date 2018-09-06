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
    if len(argv) != 3:  # Exit if not exactly one arguments  
        print '---------------------------------------------------------------------------'                               
        print "This program calculates the distance for resonances, it takes into two arguments:\n Argument 1: Distance of the ring in planet radii\n Argument 2: resonance that want to be calculated (you can put in 1:x or x:1 or x:x) then it will calculate all the resonances for x<10 "
        print ' '
        print ' Example:    '+programname+' 2.001 1:x'  
        print '---------------------------------------------------------------------------'                                    
        sys.exit(1)                                                                                                                                                                                                            
    if float(argv[1])<0:  # Exit if folder does not exist                  
        print 'ERROR: ring distance must be positive '                             
        sys.exit(1)   
    elif len(sys.argv[2].split(':'))>2:
    	print 'ERROR: resonance format not recognized '                             
        sys.exit(1)  

checkinput(sys.argv)

def calcR(f,b,dis):
	return (float(b)/float(f))**(2./3.)*dis

Rdis = float(sys.argv[1]) # ring distance
Ref = str(sys.argv[2]).split(':')[1]
Reb = str(sys.argv[2]).split(':')[0]

if 'x' in Ref:
	Ref = [float(j) for j in [i+1 for i in range(10)]]
else:
	Ref = [float(Ref)]


if 'x' in Reb:
	Reb = [float(j) for j in [i+1 for i in range(10)]]
else:
	Reb = [float(Reb)]
	

Dis=[]
for f in Ref:
	for b in Reb:
		if f==b:
			continue
		else:
			DisU=calcR(f,b,Rdis)
			print str(int(f))+":"+str(int(b))+" "+str(DisU)
			Dis.append(DisU-0.02)

print "Suggested starting positions are:"
print Dis
		

#if len(Ref)==1 and len(Reb)==1:
#	print str(Ref)+":"+str(Reb)+" "+str(calcR(Ref,Reb,Rdis))

