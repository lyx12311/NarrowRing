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
from plotScatter import *
from center_angle import *

d2r = 0.01745329251
r2d = 57.2957795131

# check command line arguments 
def checkinput(argv):                                                                       
    programname = sys.argv[0]                                                               
    if len(argv) != 3 and len(argv) !=5:  # Exit if not exactly one arguments  
    	print '---------------------------------------------------------------------------'                               
        print 'This program plots relationship between CPU time, true anomoly, number of particles and nearst neighbors for hndrag runs.\n It takes into three arguments:\n Argument 1: Directory that contains all the run directories.\n Argument 2/3: The min/max for true anomoly (no limit if left blank).\n Argument 4: Plotting style, input "line", "logx", "logy" or "loglog".'
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
nu=[] # define true anomoly
nu_in=[] # initial true anomoly
nu_end=[] # end true anomoly
for pathdir in dirnames:
	#print pathdir
	# chieck if files exist
	state1dat=pathf+"/"+pathdir+"/state1.dat"
	stream2in=pathf+"/"+pathdir+"/stream2.in"
	logdat=pathf+"/"+pathdir+"/log.dat"
	userin=pathf+"/"+pathdir+"/user.in"
	if os.path.isfile(state1dat) and os.path.isfile(stream2in) and os.path.isfile(logdat) and os.path.isfile(userin):
		# get nu of last particle from state1.dat files
		#print pathdir
		lpend=hnread(pathf+"/"+pathdir+"/state1.dat","state")
		#if pathdir=="1_1":
#			print len(lpend)
#			print lpend
#			print lpend[-1][-1]
		try:
			nu_end.append(lpend[-1][-1])
		except:
			print '------ Can\'t read state1.dat file in folder ' + pathdir
			continue
				
		# get nu of last particle from state0.dat files
		lpin=hnread(pathf+"/"+pathdir+"/state0.dat","state")
		try:
			nu_in.append(lpin[-1][-1])
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


nu=np.array(nu_end)-np.array(nu_in)

nu_c= [center_angle(i,0,360) for i in nu]

#print "NN is: "
#print len(NN)
#print "nu is: "
#print len(nu)
#print "NP is: "
#print len(NP)
#print trueAnomolyLim
# plot nu vs cpu time, color based on nearest neighbors	
plotScatter(NN,nu_c,CPUtime,'Nearest Neighbor','o',str(sys.argv[-1]))
plt.xlabel('True anamoly [degrees]')
plt.ylabel('CPU time [s]')
if limNo==1:
	plt.xlim(trueAnomolyLim)
plt.legend(loc=1,prop={'size': 6})
plt.savefig('nuvsCPU.png')


# plot nearest neighbor vs nu, color based on number of particles
plotScatter(NP,NN,nu_c,'Number of Particles','-o',str(sys.argv[-1]))
plt.xlabel('Nearest neighbor')
plt.ylabel('True anamoly [degrees]')
if limNo==1:
	plt.ylim(trueAnomolyLim)
plt.legend(loc=1,prop={'size': 6})
plt.savefig('nuvsNN.png')

# plot number of particles vs nu, color based on Nearest neighbor
plotScatter(NN,NP,nu_c,'Nearest Neighbor','-o',str(sys.argv[-1]))
plt.xlabel('Number of particles')
plt.ylabel('True anamoly [degrees]')
plt.legend(loc=1,prop={'size': 6})
if limNo==1:
	plt.ylim(trueAnomolyLim)
plt.savefig('nuvsNP.png')

plt.show()
