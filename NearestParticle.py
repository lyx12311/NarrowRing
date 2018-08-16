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
d2r = 0.01745329251
r2d = 57.2957795131

# check command line arguments 
def checkinput(argv):                                                                       
    programname = sys.argv[0]                                                               
    if len(argv) != 4:  # Exit if not exactly one arguments  
    	print '---------------------------------------------------------------------------'                               
        print 'This program plots relationship between the distance between two particles, it takes into the hnbody run folder and plotting particle numbers as argument.\n '
	print ' '
	print ' Example:    '+programname+' ./ 3 2' 
	print '---------------------------------------------------------------------------'                                    
        sys.exit(1)                                                                         
    gridfile = argv[1]                                                                                                                                    
    if not os.path.isdir(gridfile):  # Exit if folder does not exist                  
        print 'ERROR: unable to locate folder ' + gridfile                             
        sys.exit(1)                                                                            
checkinput(sys.argv)
pathf=sys.argv[1] ## put second input into file 

upPart=max([int(i) for i in [sys.argv[2],sys.argv[3]]])+1
bottomPart=min([int(i) for i in [sys.argv[2],sys.argv[3]]])+1

pathname=str(pathf)
#print pathnames
if pathname[-1]=="/":
	pathf=pathname[0:-1]

positiondiff=[]
avePositiondiff=[]
t=[]
for file in glob.glob(os.path.join(pathf,'state*.dat')):
	data=hnread(file,"state")
	LongTit = [center_angle(i,-180,180) for i in (data[:,-2]+data[:,-3])]
	positiondiff.append(center_angle(LongTit[upPart-1]-LongTit[bottomPart-1],-180,180))
	avePositiondiff.append(np.mean([center_angle(LongTit[i+1]-LongTit[i],-180,180) for i in range(len(LongTit)-1)]))
	t.append(data[0,0])
	if 'state0.dat' in str(file):	
		initialDiff=center_angle(LongTit[upPart-1]-LongTit[bottomPart-1],-180,180)
		initialDiffAve=np.mean([center_angle(LongTit[i+1]-LongTit[i],-180,180) for i in range(len(LongTit)-1)])

t, positiondiff, avePositiondiff = zip(*sorted(zip(t, positiondiff, avePositiondiff)))
positiondiff=[(i-initialDiff) for i in positiondiff]
plt.subplot(211)
plt.plot(t,positiondiff,'-o')
plt.title('Longtitude difference for particle '+ str(upPart-1) + ' and particle ' + str(bottomPart-1))
plt.xlabel('Time [yr]')
plt.ylabel('Longtitude difference [degrees]')
rangeDiff=max(positiondiff)-min(positiondiff)
plt.ylim([min(positiondiff)-0.1*rangeDiff,max(positiondiff)+0.1*rangeDiff])
plt.subplot(212)
plt.plot(t,avePositiondiff,'-o')
plt.title('Avereage longtitude difference')
plt.xlabel('Time [yr]')
plt.ylabel('Longtitude difference [degrees]')
toplim=(np.mean(avePositiondiff))-0.6*rangeDiff
bottomlim=(np.mean(avePositiondiff))+0.6*rangeDiff
if np.std(avePositiondiff) < (bottomlim-toplim)/2:
#print toplim
#print bottomlim
	plt.ylim([toplim,bottomlim])
plt.tight_layout()
plt.show()
plt.savefig(path+"/NearestParticleDis"+str(sys.argv[2])+str(sys.argv[3])+".png")   
