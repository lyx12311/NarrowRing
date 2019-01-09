#!/usr/bin/env python
##### !/usr/local/bin/python
##### !/usr/bin/python # for DPH mac
###### last updated by Lucy Lu 01/09/2019
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
from collections import Counter
from hnread import *
lengthunit=60330

def checkinput(argv):                                                                       
    programname = sys.argv[0]                                                               
    if len(argv) != 2:  # Exit if not exactly one arguments  
        print '---------------------------------------------------------------------------'                               
        print 'This program is for studying Saturn A ring mode due to interaction with Janus and Epimetheus. It takes into the mode number you want to extract from fft into as argument.\n You will need to have ran couple commands before running this code:\n elementplt.py . a 3 > outlog (creates a for the two satellites)\n FFTRingMov.py . r > outputfft (creates the fft output)\n '
        print ' '
        print ' Example:    '+programname+' 7'
	print ' Note: You will need to create a soft link to link to this file in the folder you are trying to run this code in\n'  
        print '---------------------------------------------------------------------------'                                    
        sys.exit(1)                                                                         
                                                                    
aout='1'
# check error
checkinput(sys.argv)

npart,inia=hnread('stream2.in','stream',[],aout)
print(inia)

reson=int(sys.argv[1])
with open('outlog') as f:
	parts=f.readlines()
	data=[]
	for line in parts[3:len(parts)]:
		linest=line.split()
		if int(linest[0])!=1:
			data.append([float(j) for j in linest])
data=np.array(data)

N=data[:,0]-data[0,0]
td=data[:,1]
ad=data[:,2]
bodyN=Counter(N).keys()
t=[[] for i in range(len(bodyN))]
a=[[] for i in range(len(bodyN))]
#print(t)
for i in range(len(N)):
	t[int(N[i])].append(td[i])
	a[int(N[i])].append(ad[i]*lengthunit)

for i in bodyN[0:2]:
	plt.subplot(2,1,1)	
	plt.plot(t[int(i)],a[int(i)])
	plt.ticklabel_format(useOffset=False)
	plt.xlabel('time [yr]')
	plt.ylabel('Distant from planet [km]')
	
print(a[0][0],a[1][0])
	
	
## second subplot
datax=[]
datay=[]
with open('outputfft') as f:
	parts=f.readlines()
	for line in parts[2:len(parts):2]:
		#print line
		linest=line.split()
		datax.append([float(j) for j in linest])
	for line2 in parts[3:len(parts):2]:
		linest=line2.split()
		datay.append([float(j) for j in linest])
		
#data=np.array(data)
#print datax
#print datay
apendx=[]
apendy=[]
for i in range(len(datax)):
	checkx=datax[i]
	for j in range(len(checkx)):
		if int(checkx[j])==reson:
			apendx.append(checkx[j])
			apendy.append(datay[i][j])
#print(max(t[0]))
plt.subplot(2,1,2)
plt.plot(np.linspace(float(min(t[0])),float(max(t[0])),num=len(apendy)),[i*inia*lengthunit for i in apendy])
#plt.ylim([0,0.0002])
plt.xlabel('time [yr]')
plt.ylabel('FFT ae [km] of m='+str(reson)) # this a is from stream.in, not accurate after correcting for J2 but approximately correct
plt.tight_layout()
plt.savefig("Ana_"+str(reson)+".png")

#plt.show()	
