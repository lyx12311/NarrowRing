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
from unevenfft import *
from unevenfft_res import *
from TimeGenerate import *
d2r = 0.01745329251
r2d = 57.2957795131

def checkinput(argv):                                                                       
    programname = sys.argv[0]                                                               
    if len(argv) != 3:  # Exit if not exactly one arguments  
    	print '---------------------------------------------------------------------------'                               
        print "This program creates a movie of the fft of the ring vs time based on hnbody state files.\n It takes into two arguments: \n Argument 1: Folder name \n Argument 2: Output type -- no output (0), print out r peaks (r), print out z peaks (z)\n"
	print ' '
	print ' Example:    '+programname+' m1 0'  
	print '---------------------------------------------------------------------------'                                    
        sys.exit(1)                                                                         
    gridfile = argv[1]                                                                                                                                    
    if not os.path.isdir(gridfile):  # Exit if folder does not exist                  
        print 'ERROR: unable to locate folder ' + gridfile                             
        sys.exit(1)   

checkinput(sys.argv)
outputInt = str(sys.argv[-1])
if outputInt=='z':
	print "z peak heights are"
	Opt=1
	outputInt=1
elif outputInt=='r':
	print "r peak heights are"
	Opt=1
	outputInt=0
elif outputInt=='0':
	Opt=0
else:
	print "output type not recognized!"
	sys.exit(1)
	

path=sys.argv[1] ## put second input into file 
pathname=str(path)
os.system("mkdir "+str(path)+"/pngfiles")
if Opt==0:
	print pathname
if pathname[-1]=="/":
	path=pathname[0:-1]
try:
	numbpart=hnread(pathname+"/stream2.in","stream")
except:
	try:
		numbpart=hnread(pathname+"/stream.in","stream")
	except:
		print "Can't find stream.in or stream2.in file"
		sys.exit(1)
print "number of particles: "+str(numbpart)
#print numbpart
# count files
numfile=0
for file in glob.glob(os.path.join(path,'state*.dat')):
	numfile+=1
	
if Opt==0:
	print "Total number of files: " +str(numfile)	
numfilec=0

statenum=[]
filenames=[]
for files in glob.glob(os.path.join(path,'state*.dat')):
	filenames.append(files)
	#print files.split('.')
	statenum.append(float(files.split('.')[-2].split('te')[1]))

statenum,filenames=zip(*sorted(zip(statenum,filenames)))

for file in filenames:
	numfilec+=1
	#print file
	if Opt==0:
		if int(float(numfilec)/numfile*100)-int(float(numfilec-1)/numfile*100)!=0:
			print str(int(float(numfilec)/numfile*100))+"% done"
	#print file
	name = file.split('/')
	#print name
	PNGName = str(name[-1])
	try:
		unevenfft(file,numbpart*10,10,10,Opt,outputInt)
		#unevenfft_res(file,numbpart*10,10,10,Opt,outputInt)
		#print str(path)+"/pngfiles/"+PNGName+'.png'
		plt.savefig(str(path)+"/pngfiles/"+PNGName+'.png')
		plt.close()
	except BaseException as e:
		print e
		if Opt==0:
			print "Warning: Can't fft file "+str(file)
		continue

#	unevenfft(file,numbpart*10,10,10,outputInt)
##	unevenfft(file,10000,5,10,1)
#	plt.savefig(str(path)+"/pngfiles/"+PNGName+'.png')
#	plt.close()

FolderName=path.split('/')
if FolderName[-1]=='.':
	#print("ffmpeg -framerate 10 -i "+ str(path)+"/pngfiles/"+"state%d.dat.png -loglevel warning -pix_fmt yuv420p -y "+NameRotNRot[int(sys.argv[2])]+"_"+NameLinPol[int(sys.argv[3])]+".mp4")
	os.system("ffmpeg -framerate 10 -i "+str(path)+"/pngfiles/"+"state%d.dat.png -loglevel warning -pix_fmt yuv420p -y " + "fft.mp4")
	#print 1
else:
	os.system("ffmpeg -framerate 10 -i "+ str(path)+"/pngfiles/state%d.dat.png -loglevel warning -pix_fmt yuv420p -y "+FolderName[-1]+".mp4")
	os.system("mv "+FolderName[-1]+".mp4 "+str(path))

os.system("rm -rf "+str(path)+"/pngfiles")
