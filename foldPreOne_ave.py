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
prectype={"W":[-4,-180,180,'Longtitude of Ascending Node [degrees]'],"w":[-3,0,360,'Longtitude of Pericenter [degrees]']}

d2r = 0.01745329251
r2d = 57.2957795131

# check command line arguments 
def checkinput(argv):                                                                       
    programname = sys.argv[0]                                                               
    if len(argv) != 3:  # Exit if not exactly one arguments  
    	print '---------------------------------------------------------------------------'                               
        print 'This program plots time vs pericenter longtitude to check precession in one folder. \n It takes into 3 arguments:\n Argument 1: Run directory.\n Argument 2: sort by particle numbers ("NP"), Nearest neighbors ("NN").\n Argument 3: pericenter precession ("w") or nodal precession ("W").'
	print ' '
	print ' Example:    '+programname+' ./ NN w' 
	print '---------------------------------------------------------------------------'                                    
        sys.exit(1)                                                                         
    gridfile = argv[1]                                                                                                                                    
    if not os.path.isdir(gridfile):  # Exit if folder does not exist                  
        print 'ERROR: unable to locate folder ' + gridfile                             
        sys.exit(1)                                                                            
checkinput(sys.argv)

pathf=sys.argv[1] ## put second input into file 
sortby=sys.argv[2]
wW=sys.argv[3]	
pathname=str(pathf)
#print pathname
if pathname[-1]=="/":
	pathf=pathname[0:-1]

print('getting folders')
fn=[x[0] for x in os.walk(pathf)]
fn=fn[1:len(fn)]
#print fn
Mn=[]
NP=[]

print titletype[sortby]+"      Mode numbers      precession [degrees]"
prec_ave=[]
#plt.figure()
for fpath in fn:
	pers=[]
	try:
		for file in glob.glob(os.path.join(fpath,'body*.dat')):
			if file.split('/')[-1]=='body0.dat':
				continue
			#print(file)
			# get closest of last particle from state1.dat files
			lpend=hnread(file,"body")
			r_end=lpend[:,1]*(1.-lpend[:,2]*lpend[:,2])/(1+lpend[:,2]*np.cos(lpend[:,-1]*d2r))
			LongTit = lpend[:,prectype[wW][0]]
			LongTit_cent=[(center_angle(i,-180,180)) for i in LongTit]
			timeplt=lpend[:,0]

			zippedData=zip(timeplt,LongTit_cent)
			zippedData.sort()
			tp_s,L_s=zip(*zippedData)

			pers1=L_s[-1]-L_s[1]
			pers.append(center_angle(pers1,-180,180))
		printper=np.array(pers).mean()
		prec_ave.append(printper)
		Mn1=int(fpath.split('/')[-1])-1
		Mn.append(Mn1)
		for streamf in glob.glob(os.path.join(fpath,filenametype[sortby])):
			NP1=hnread(streamf,sorttype[sortby])
			NP.append(NP1)
			break
		print str(NP1)+"      "+str(Mn1)+"      "+str(center_angle(printper,prectype[wW][1]-0.5,prectype[wW][2]-0.5))
	except BaseException as e:
		print e
		continue
	

plotScatter(NP,Mn,[center_angle(i,prectype[wW][1]-0.5,prectype[wW][2]-0.5) for i in prec_ave],titletype[sortby],'o',"line")
plt.xlabel('Mode Number')
plt.legend(loc=2)
plt.ylabel('Precession in 5 Years [degrees]')
plt.savefig('TimevsLP_onepart_sum.png')

plt.show()
