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

titletype={"PN":"Particle Numbers","NN":"Nearest Neighbors"}
sorttype={"PN":"stream","NN":"user"}
filenametype={"PN":"stream*","NN":"user.in"}

d2r = 0.01745329251
r2d = 57.2957795131

# check command line arguments 
def checkinput(argv):                                                                       
    programname = sys.argv[0]                                                               
    if len(argv) != 3:  # Exit if not exactly one arguments  
    	print '---------------------------------------------------------------------------'                               
        print 'This program plots time vs pericenter longtitude to check precession in one folder. \n It takes into two arguments:\n Argument 1: Run directory.\n Argument 2: sort by particle numbers ("NP"), Nearest neighbors ("NN")'
	print ' '
	print ' Example:    '+programname+' ./ NN' 
	print '---------------------------------------------------------------------------'                                    
        sys.exit(1)                                                                         
    gridfile = argv[1]                                                                                                                                    
    if not os.path.isdir(gridfile):  # Exit if folder does not exist                  
        print 'ERROR: unable to locate folder ' + gridfile                             
        sys.exit(1)                                                                            
checkinput(sys.argv)

pathf=sys.argv[1] ## put second input into file 
sortby=sys.argv[2]
	
pathname=str(pathf)
#print pathname
if pathname[-1]=="/":
	pathf=pathname[0:-1]

fn=[x[0] for x in os.walk(pathf)]
fn=fn[1:len(fn)]
#print fn
pers=[]
Mn=[]
NP=[]

print titletype[sortby]+"      Mode numbers      precession [degrees]"

plt.figure()
for fpath in fn:
	try:
		for file in glob.glob(os.path.join(fpath,'body1.dat')):
			# get closest of last particle from state1.dat files
			lpend=hnread(file,"body")
			r_end=lpend[:,1]*(1.-lpend[:,2]*lpend[:,2])/(1+lpend[:,2]*np.cos(lpend[:,-1]*d2r))
			#LongTit = lpend[:,-2]+lpend[:,-3]
			LongTit = lpend[:,-3]
			LongTit_cent=[(center_angle(i,-1,359)) for i in LongTit]
			#print "this is lpend[]"+str(lpend[:,0])
			timeplt=lpend[:,0]

		zippedData=zip(timeplt,LongTit_cent)
		zippedData.sort()
		tp_s,L_s=zip(*zippedData)

		plt.plot(tp_s,L_s-L_s[0],label= "M = "+str(int(fpath.split('/')[-1])-1))
		pers1=L_s[-1]-L_s[0]
		pers.append(pers1)
		Mn1=int(fpath.split('/')[-1])-1
		Mn.append(Mn1)
		for streamf in glob.glob(os.path.join(fpath,filenametype[sortby])):
			NP1=hnread(streamf,sorttype[sortby])
			NP.append(NP1)
			break
		print str(NP1)+"      "+str(Mn1)+"      "+str(center_angle(pers1,-1.,359.))
	except BaseException as e:
		print e
		continue
	
#print Mn
#print pers	
plt.xlabel('Time [yr]')
plt.ylabel('Longtitude of pericenter [degrees]')
plt.ylim([-20,120])
#plt.legend(loc='upper left')
plt.savefig('TimevsLP_onepart.png')


plotScatter(NP,Mn,[center_angle(i,0,360) for i in pers],titletype[sortby],'o',"line")
#plt.plot(Mn,[center_angle(i,-180,180) for i in pers],'ro')
plt.xlabel('Mode Number')
#plt.ylim([-20,120])
plt.ylabel('Precession in 5 Years [degrees]')
plt.savefig('TimevsLP_onepart_sum.png')

plt.show()
