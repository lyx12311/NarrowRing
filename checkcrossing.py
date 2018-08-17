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
import scipy.fftpack
from hnread import *
from center_angle import *

d2r = 0.01745329251
r2d = 57.2957795131

# check command line arguments 
def checkinput(argv):                                                                       
    programname = sys.argv[0]                                                               
    if len(argv) != 2:  # Exit if not exactly one arguments  
    	print '---------------------------------------------------------------------------'                               
        print 'This program checks if the particles crossed each other, it takes into the hnbody run folder as argument.\n '
	print ' '
	print ' Example:    '+programname+' ./' 
	print '---------------------------------------------------------------------------'                                    
        sys.exit(1)                                                                         
    gridfile = argv[1]                                                                                                                                    
    if not os.path.isdir(gridfile):  # Exit if folder does not exist                  
        print 'ERROR: unable to locate folder ' + gridfile                             
        sys.exit(1)                                                                            
checkinput(sys.argv)
pathf=sys.argv[1] ## put second input into file 

pathname=str(pathf)
#print pathnames
if pathname[-1]=="/":
	pathf=pathname[0:-1]

positiondiff=[]
avePositiondiff=[]
t=[]
crossp=0
for file in glob.glob(os.path.join(pathf,'state*.dat')):
	data=hnread(file,"state")
	t=data[0,0]
	LongTit = [center_angle(i,-180,180) for i in (data[:,-2]+data[:,-3])]
	Longdiff = [center_angle(LongTit[i+1]-LongTit[i],-180,180) for i in range(len(LongTit)-1)]
	signdiff=np.sign(Longdiff)
	sign_reff=np.sign(sum(signdiff))
	for i in signdiff:
		if i == -sign_reff:
			print "particle crossed at time "+str(t)
			crossp=crossp+1

if crossp==0:
	print "all particles stayed in order"
		
		
	#print signdiff
	
		
	
	
