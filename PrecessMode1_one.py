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
from hnread import *
from center_angle import *
from plotScatter import *

d2r = 0.01745329251
r2d = 57.2957795131

# check command line arguments 
def checkinput(argv):                                                                       
    programname = sys.argv[0]                                                               
    if len(argv) != 2:  # Exit if not exactly one arguments  
    	print '---------------------------------------------------------------------------'                               
        print 'This program plots time vs pericenter longtitude to check precession. \n It takes into one arguments to be the run directory.'
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

try:
	trueAnomolyLim=[float(sys.argv[2]),float(sys.argv[3])]
	limNo=1
except:
	print "No limit for plotting"
	limNo=2
	
pathname=str(pathf)
#print pathname
if pathname[-1]=="/":
	pathf=pathname[0:-1]


closR_end=[] # define closest particle
Lon_end=[] # closest approach longtitde 
timeplt=[] # time

for file in glob.glob(os.path.join(pathf,'state*.dat')):
	# get closest of last particle from state1.dat files
	lpend=hnread(file,"state")
	r_end=lpend[:,1]*(1.-lpend[:,2]*lpend[:,2])/(1+lpend[:,2]*np.cos(lpend[:,-1]*d2r))
	LongTit = lpend[:,-2]+lpend[:,-3]
	LongTit_cent=[(center_angle(i,-180.,180.)) for i in LongTit]
	
	### method that only consider the min
	#print min(r_end)
	#print LongTit_cent[r_end.argmin()]
	closR_end.append(min(r_end))
	Lon_end.append(LongTit_cent[r_end.argmin()])
	
	
	## method that fits poly
#	# how many points to take to fit
#	ptt=3
#	zippedData=zip(r_end,LongTit_cent)
#	zippedData.sort()
#	r_end,LongTit_cent=zip(*zippedData)
#	
#	r_end=np.array(r_end)
#	LongTit_cent=np.array(LongTit_cent)
#	
#	polyfitDat = np.polyfit(LongTit_cent[0:ptt], r_end[0:ptt], 2)
#	
#	# Long of the min
#	LM=-polyfitDat[1]/(2*polyfitDat[0])
#	# min r
#	MR=polyfitDat[0]*LM**2+polyfitDat[1]*LM+polyfitDat[2]
#	
#	closR_end.append(MR)
#	Lon_end.append(LM)
	timeplt.append(lpend[0,0])


# precession rate vs CPUtime
plt.figure()

zippedData=zip(timeplt,Lon_end)
zippedData.sort()
tp_s,L_s=zip(*zippedData)

plt.plot(tp_s,L_s,'-o')
plt.xlabel('Time [yr]')
plt.ylabel('Longtitude of pericenter [degrees]')
plt.savefig('TimevsLP.png')

# precession rate vs number of nearest neighbors
plt.figure()

zippedData=zip(timeplt,closR_end)
zippedData.sort()
tpR_s,R_s=zip(*zippedData)

plt.plot(tpR_s,R_s,'-o')
plt.xlabel('Time [yr]')
plt.ylabel('Closest approach radii [planet radii]')
plt.savefig('TimevsCR.png')

plt.show()
