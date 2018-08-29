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
from TimeGenerate import *
d2r = 0.01745329251
r2d = 57.2957795131

def checkinput(argv):                                                                       
    programname = sys.argv[0]                                                               
    if len(argv) != 2 and len(argv) != 3:  # Exit if not exactly one arguments  
    	print '---------------------------------------------------------------------------'                               
        print "This program creates a movie of the fft of the ring vs time based on hnbody state files.\n It takes into the folder name as argument \n Add 0 to the end if you don't want output"
	print ' '
	print ' Example:    '+programname+' m1 0'  
	print '---------------------------------------------------------------------------'                                    
        sys.exit(1)                                                                         
    gridfile = argv[1]                                                                                                                                    
    if not os.path.isdir(gridfile):  # Exit if folder does not exist                  
        print 'ERROR: unable to locate folder ' + gridfile                             
        sys.exit(1)   

checkinput(sys.argv)

if len(sys.argv)==3:
	outputInt=0
else:
	outputInt=1
	
if outputInt==1:
	print "peak heights are"

path=sys.argv[1] ## put second input into file 
pathname=str(path)
os.system("mkdir "+str(path)+"/pngfiles")
if outputInt==0:
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
#print numbpart
# count files
numfile=0
for file in glob.glob(os.path.join(path,'state*.dat')):
	numfile+=1
	
if outputInt==0:
	print "Total number of files: " +str(numfile)	
numfilec=0
for file in glob.glob(os.path.join(path,'state*.dat')):
	numfilec+=1
	#print file
	if outputInt==0:
		if int(float(numfilec)/numfile*100)-int(float(numfilec-1)/numfile*100)!=0:
			print str(int(float(numfilec)/numfile*100))+"% done"
	#print file
	name = file.split('/')
	#print name
	PNGName = str(name[-1])
	try:
		unevenfft(file,numbpart*10,10,10,outputInt)
		#print str(path)+"/pngfiles/"+PNGName+'.png'
		plt.savefig(str(path)+"/pngfiles/"+PNGName+'.png')
		plt.close()
	except:
		if outputInt==0:
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

#os.system("rm -rf "+str(path)+"/pngfiles")
