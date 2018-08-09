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
    if len(argv) != 5 and len(argv) !=3:  # Exit if not exactly one arguments  
    	print '---------------------------------------------------------------------------'                               
        print 'This program plots relationship between CPU time, precession (rate), number of particles and nearst neighbors for hndrag runs.\n It takes into four arguments:\n Argument 1: Directory that contains all the run directories.\n Argument 2/3: The min/max for precession rate (no limit if left blank).\n Argument 4: Plotting style, input "line", "logx", "logy" or "loglog".'
	print ' '
	print ' Example:    '+programname+' ./' + ' logx' 
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

dirnames=[]
for dirname in os.listdir(pathf):
	if os.path.isdir(dirname):
		dirnames.append(dirname)
#print dirnames

print str(len(dirnames)) + ' run directories detected!'



NP=[] # define number of particles
CPUtime=[] # define running time
NN=[] # define nearest neighbor counts
closR_end=[] # define closest particle
closR_in=[] # same as above
Lon_end=[] # closest approach longtitde 
Lon_in=[] # same as above
for pathdir in dirnames:
	#print pathdir
	# chieck if files exist
	state1dat=pathf+"/"+pathdir+"/state1.dat"
	stream2in=pathf+"/"+pathdir+"/stream2.in"
	logdat=pathf+"/"+pathdir+"/log.dat"
	userin=pathf+"/"+pathdir+"/user.in"
	if os.path.isfile(state1dat) and os.path.isfile(stream2in) and os.path.isfile(logdat) and os.path.isfile(userin):
		# get closest of last particle from state1.dat files
		lpend=hnread(pathf+"/"+pathdir+"/state1.dat","state")
		r_end=lpend[:,1]*(1.-lpend[:,2]*lpend[:,2])/(1+lpend[:,2]*np.cos(lpend[:,-1]*d2r))
		LongTit = lpend[:,-2]+lpend[:,-3]
		LongTit_cent=[(center_angle(i,-180.,180.)) for i in LongTit]
		#print min(r_end)
		#print LongTit_cent[r_end.argmin()]
		try:
			closR_end.append(min(r_end))
			Lon_end.append(LongTit_cent[r_end.argmin()])
		except:
			print '------ Can\'t read state1.dat file in folder ' + pathdir
			continue
				
		# get closest of last particle from state0.dat files
		lpin=hnread(pathf+"/"+pathdir+"/state0.dat","state")
		r_in=lpin[:,1]*(1.-lpin[:,2]*lpin[:,2])/(1+lpin[:,2]*np.cos(lpin[:,-1]*d2r))
		LongTit = lpin[:,-2]+lpin[:,-3]
		LongTit_cent=[(center_angle(i,-180.,180.)) for i in LongTit]
		try:
			closR_in.append(min(r_in))
			Lon_in.append(LongTit_cent[r_in.argmin()])
		except:
			print '------ Can\'t read state0.dat file in folder ' + pathdir
			continue
		
					
		# get number of particles from stream2.in files
		try:
			NP.append(hnread(pathf+"/"+pathdir+"/stream2.in","stream"))
		except:
			print '------ Can\'t read stream2.in file in folder ' + pathdir
			continue 
	
		# get nearest neighbor counts from user.in files
		try:
			NN.append(hnread(pathf+"/"+pathdir+"/user.in","user"))
		except:
			print '------ Can\'t read user.in file in folder ' + pathdir
			continue 
		
		# get CPU time of particles from log.dat files
		try:
			CPUtime.append(hnread(pathf+"/"+pathdir+"/log.dat","log"))
		except:
			print '------ Can\'t read log.dat file in folder ' + pathdir
			continue
	else:
		print "------ Can\'t gather all files in folder " + pathdir
		continue


timediff = abs(lpend[0,0]-lpin[0,0])
Londiff = abs(np.array(Lon_end)-np.array(Lon_in))
perRate = [abs(i/timediff) for i in Londiff]
#print "NN is: "
#print len(NN)
#print "nu is: "
#print len(nu)
#print "NP is: "
#print len(NP)

# precession rate vs CPUtime
plotScatter(NN,perRate,CPUtime,'Nearest Neighbor','o',str(sys.argv[-1]))
plt.xlabel('Precession Rate [degrees/s]')
plt.ylabel('CPU time [s]')
if limNo==1:
	plt.xlim(trueAnomolyLim)
plt.legend(loc=1,prop={'size': 6})
plt.savefig('CPUvsPR.png')


# precession rate vs number of nearest neighbors
plotScatter(NP,NN,perRate,'Number of Particles','-o',str(sys.argv[-1]))
plt.xlabel('Nearest neighbor')
plt.ylabel('Precession Rate [degrees/s]')
if limNo==1:
	plt.ylim(trueAnomolyLim)
plt.legend(loc=1,prop={'size': 6})
plt.savefig('PRvsNN.png')

# precession rate vs number of particle
plotScatter(NN,NP,perRate,'Nearest Neighbor','-o',str(sys.argv[-1]))
plt.xlabel('Number of particles')
plt.ylabel('Precession Rate [degrees/s]')
plt.legend(loc=1,prop={'size': 6})
if limNo==1:
	plt.ylim(trueAnomolyLim)
plt.savefig('PRvsNP.png')

# precession degree vs number of particle
plotScatter(NN,NP,Londiff,'Nearest Neighbor','-o',str(sys.argv[-1]))
plt.xlabel('Number of particles')
plt.ylabel('Precession [degrees]')
plt.legend(loc=1,prop={'size': 6})
if limNo==1:
	plt.ylim([i*timediff for i in trueAnomolyLim])
plt.savefig('PvsNP.png')

plt.show()
