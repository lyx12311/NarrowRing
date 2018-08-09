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

d2r = 0.01745329251
r2d = 57.2957795131


# check command line arguments 
def checkinput(argv):                                                                       
    programname = sys.argv[0]                                                               
    if len(argv) != 3:  # Exit if not exactly one arguments  
    	print '---------------------------------------------------------------------------'                               
        print 'This program plots the delta true anomoly / true anomoly vs CPU time for hndrag runs.\n It also determins the shortest distance from the origin and determine the optimized number of particles, nearest neighbors, etc.\n It takes into two arguments:\n Argument 1: The directory contains all the run directories.\n Argument 2: Mode of true anomoly to be real true anomoly (0), Highest particle number true anomoly to be real true anomoly (1).'
	print ' '
	print ' Example:    '+programname+' ./ 1' 
	print '*Note: If the final diagnostic particle number is smaller than the nearest neighbor calculated, the program goes to the next result that is the most accurate'
	print '---------------------------------------------------------------------------'                                    
        sys.exit(1)                                                                         
    gridfile = argv[1]                                                                                                                                    
    if not os.path.isdir(gridfile):  # Exit if folder does not exist                  
        print 'ERROR: unable to locate folder ' + gridfile                             
        sys.exit(1)                                                                            
checkinput(sys.argv)
pathf=sys.argv[1] ## put second input into file 
pathname=str(pathf)
print pathname
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
nu=[] # define true anomoly

for pathdir in dirnames:
	#print pathdir
	# chieck if files exist
	state1dat=pathf+"/"+pathdir+"/state1.dat"
	stream2in=pathf+"/"+pathdir+"/stream2.in"
	logdat=pathf+"/"+pathdir+"/log.dat"
	userin=pathf+"/"+pathdir+"/user.in"
	if os.path.isfile(state1dat) and os.path.isfile(stream2in) and os.path.isfile(logdat) and os.path.isfile(userin):
		# get nu of last particle from state1.dat files
		with open(pathf+"/"+pathdir+"/state1.dat") as sf:
			parts=sf.readlines()
			lp=parts[-1].split()
			try:
				nu.append(float(lp[-1]))
			except:
				print '------ warning: Can\'t read state1.dat file in folder ' + pathdir
				continue
			
		# get number of particles from stream2.in files
		with open(pathf+"/"+pathdir+"/stream2.in") as stf:
			parts=stf.readlines()
			numbP=parts[5].split()
			try:
				NP.append(float(numbP[2]))
			except:
				print '------ warning: Can\'t read stream2.in file in folder ' + pathdir
				continue 
			
	
		# get nearest neighbor counts from input.hnb files
		with open(pathf+"/"+pathdir+"/user.in") as uf:
			parts=uf.readlines()
			NearN=parts[-6].split()
			try:
				NN.append(float(NearN[-1]))
			except:
				print '------ warning: Can\'t read user.in file in folder ' + pathdir
				continue 
		
		# get CPU time of particles from log.dat files
		with open(pathf+"/"+pathdir+"/log.dat") as logf:
			parts=logf.readlines()
			cputime=parts[-2].split()
			try:
				CPUtime.append(float(cputime[4]))
			except:
				print '------ warning: Can\'t read log.dat file in folder ' + pathdir
				continue
	else:
		print "------ warning: Can\'t gather all files in folder " + pathdir
		continue
		
#	print len(NP)
#	print len(NN)
#	print len(CPUtime)
#	print " "
	
#print len(NP)
#print len(NN)
#print len(CPUtime)

if int(sys.argv[2])==1:
	zippedData=zip(NP,NN,CPUtime,nu)
	zippedData.sort()
	NP,NN,CPUtime,nu=zip(*zippedData)
	truenu=nu[-1]
elif int(sys.argv[2])==0:
	truenu = max(set(nu), key=nu.count)
else:
	print 'second argument only takes 0 and 1'
	sys.exit(1)
print 'Mode of true anomoly is: '+str(truenu)
sqrtdist=[] # finding the optimized nu and cputime
for i in range(len(CPUtime)):
	sqrtdist.append(np.sqrt(abs(truenu-nu[i])**2+CPUtime[i]**2))

zippedData=zip(sqrtdist,NN,NP,CPUtime,nu)
zippedData.sort()
sqrtdist,NN,NP,CPUtime,nu=zip(*zippedData)
#print sqrtdist
for i in range(len(NN)):
	if NN[i]>NP[i]:
		continue
	else:
		NNfin=NN[i]
		NPfin=NP[i]
		CPUtimefin=CPUtime[i]
		nufin=nu[i]
		break
plt.figure()
plt.scatter([abs(i-truenu) for i in nu],CPUtime)		

#plt.colorbar()	
plt.ylabel('CPU time [s]')
plt.xlabel('delta True anomoly / True anomoly')
#plt.legend(loc=2,prop={'size': 6})
#plt.figure()
#plt.scatter(nu,CPUtime)
plt.savefig('DeltanunuvsCPU.png')
print '---------------------------------------------------------------------------' 
print 'Optimized parameter is:\n   Nearest neighbors: ' + str(NN[0])+'\n   Particle numbers: ' + str(NP[0]) + '\n This gives a total CPU hours of ' + str(CPUtime[0]) + ' s, and true anomoly error of ' + str(abs((nu[0]-truenu)/truenu)*100) + '%'                                    
print 'Optimized parameter nearest neighbor < particle number is:\n   Nearest neighbors: ' + str(NNfin)+'\n   Particle numbers: ' + str(NPfin) + '\n This gives a total CPU hours of ' + str(CPUtimefin) + ' s, and true anomoly error of ' + str(abs((nufin-truenu)/truenu)*100) + '%'
print '---------------------------------------------------------------------------'                               
        
#plt.figure()
#plt.scatter(NN,nu)
#plt.xlabel('Nearest neighbor')
#plt.ylabel('True anomoly [degrees]')
#plt.savefig('nuvsNN.png')
#
#plt.figure()
#plt.scatter(NP,nu)
#plt.xlabel('Number of particles')
#plt.ylabel('True anomoly [degrees]')
#plt.savefig('NPvsNN.png')

#plt.show()
