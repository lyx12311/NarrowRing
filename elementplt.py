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
from plotScatter import *
from chkEle import *
from getEle import *

def checkinput(argv):                                                                       
    programname = sys.argv[0]                                                               
    if len(argv) != 4:  # Exit if not exactly one arguments  
    	print '---------------------------------------------------------------------------'                               
        print "This program plots sample particle element vs time for a ring based on hnbody body files.\n It takes into 3 arguments:\n Argument 1: the folder name\n Argument 2: element to plot ('a','e','i',etc.. [see chkEle.py for more info])\n Argument 3: how many particles to plot\n"
	print ' '
	print ' Example:    '+programname+' m1 e 10'  
	print '---------------------------------------------------------------------------'                                    
        sys.exit(1)                                                                         
    gridfile = argv[1]                                                                                                                                    
    if not os.path.isdir(gridfile):  # Exit if folder does not exist                  
        print 'ERROR: unable to locate folder ' + gridfile                             
        sys.exit(1)   

checkinput(sys.argv)


## how many particles to plot
ptp=int(sys.argv[3])
## element number
elem=str(sys.argv[2])
ele_n=geteleInd(str(sys.argv[2]))


path=sys.argv[1] ## put second input into file 
pathname=str(path)
print pathname
if pathname[-1]=="/":
	path=pathname[0:-1]

# count and sort files
numfile=0
filename=[]
filenumb=[]
for file in glob.glob(os.path.join(path,'body*.dat')):
	numfile+=1
	filename_one =(file.split('/'))[-1]
	filename.append(str(file))
	filenumb.append(filename_one.split('y')[-1].split('.')[-2])

filenumb, filename = zip(*sorted(zip([int(i) for i in filenumb],filename)))
#print filenumb
#print filenumb
#print filename
#print filenumb
filetp = filename[0:len(filename):int(len(filename)/ptp)]
filenp = filenumb[0:len(filename):int(len(filename)/ptp)]
#print filenp
#print filetp

if len(filetp)!=ptp:
	print "Optimized to plot "+ str(len(filetp))+" plots instead of "+str(ptp)+" plots!"
	
#print filetp

subplotNum = int(math.ceil(ptp**0.5))

#print subplotNum
fig, axes = plt.subplots(nrows=subplotNum, ncols=subplotNum,figsize=(ptp, 0.7*ptp))
subplotnumber=1
for file in filetp:
	plt.subplot(subplotNum,subplotNum,subplotnumber)
	#print getEle(file,"t")
	
	plt.plot(getEle(file,"t"),getEle(file,elem))
	plt.xlabel('Time [yr]')
	plt.ylabel(str(sys.argv[2])+str(filenp[subplotnumber-1]))
	#print subplotnumber
	subplotnumber=subplotnumber+1

#fig.suptitle(str(sys.argv[2])+"vs time for "+str(len(filetp))+" particles", fontsize=ptp*2)	
fig.tight_layout() # 
plt.savefig(path+"/element_"+str(sys.argv[2])+"_"+str(len(filetp))+".png")	
#plt.show()
