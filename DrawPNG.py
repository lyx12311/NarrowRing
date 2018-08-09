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

d2r = 0.01745329251
r2d = 57.2957795131
plotRange=0.5 # the range seeing
printdes=4 # print out time desimals
## sys.argv: a list of strings
### sys.argv[0] : name of script 
### sys.argv[1]: folder name
### sys.argv[2]: non-rotating frame -> 0, rotating frame -> 1
## sys.argv[3]: linear plot -> 0, polar plot -> 1
# check command line arguments 
headerline=18
NameRotNRot=["Rot","NRot"]
NameLinPol=["Lin","Pol"]  
                                                           
def checkinput(argv):                                                                       
    programname = sys.argv[0]                                                               
    if len(argv) != 4:  # Exit if not exactly one arguments  
    	print '---------------------------------------------------------------------------'                               
        print 'This program creates a movie based on hnbody state files.\n It takes into 3 arguments.\n First argument: the folder name \n Second argument: non-rotating frame (0) or rotating frame (1) \n Third argument: linear plot (0) or polar plot (1)'
	print ' '
	print ' Example:    '+programname+' M1 0 0'  
	print '---------------------------------------------------------------------------'                                    
        sys.exit(1)                                                                         
    gridfile = argv[1]                                                                                                                                    
    if not os.path.isdir(gridfile):  # Exit if folder does not exist                  
        print 'ERROR: unable to locate folder ' + gridfile                             
        sys.exit(1)                                                                            

def calc_r(a,e,nu):
	return a*(1.-e*e)/(1.+e*np.cos(nu*d2r))

def calc_dr(a,e,nu,a_r,e_r):
	return a*(1.-e*e)/(1.+e*np.cos(nu*d2r))-a_r*(1.-e_r*e_r)/(1.+e_r*np.cos(nu*d2r))
	
def calc_z(a,e,i,w,nu,omega):
	return a*(1.-e*e)/(1.+e*np.cos(nu*d2r))*np.sin(i*d2r)*np.sin((w-omega+nu)*d2r)
		
def center_angle(x,minc,maxc): # this can only handle angles in degrees with semetric bounds around 0 or bounds greater than 0
	if x >= minc and x <= maxc:
		remain = x
	else:
		rangex = maxc-minc
		if x < 0:
			remain = x + math.ceil(abs(x)/rangex)*rangex
			#print x
		else:
#			rescale = (x)/rangex
#			remain = (rescale-int(rescale))*rangex
			remain = x - math.ceil(abs(x)/rangex)*rangex
	return remain


# check error
checkinput(sys.argv)



path=sys.argv[1] ## put second input into file 
pathname=str(path)
os.system("mkdir "+str(path)+"/pngfiles")
print pathname
if pathname[-1]=="/":
	path=pathname[0:-1]

####### calculates the reference semimajor axis and eccentricity from first state file
a = []
e = []
radiusfirstfile=[]
zfirstfile = []
with open(path+'/state1.dat') as firstFile:
		i=0;
		while i<headerline:
			next(firstFile)
			i=i+1
		for line in firstFile:
			parts=line.split()
			a.append(float(parts[1]))
			e.append(float(parts[2]))
			mean1=float(parts[6])
			radiusfirstfile.append(calc_r(float(parts[1]),float(parts[2]),float(parts[-1])))
			zfirstfile.append(calc_z(float(parts[1]),float(parts[2]),float(parts[3]),float(parts[5]),float(parts[-1]),float(parts[4])))
a_ave=np.mean(a)
e_ave=np.mean(e)
z_ave=np.mean(zfirstfile)

### define min and max for plotting
maxSemiAxis=max(a)
minSemiAxis=min(a)
maxr=max(radiusfirstfile)
minr=min(radiusfirstfile)
maxz=max(zfirstfile)
minz=min(zfirstfile)
maxdr=0
mindr=0

numfile=0
####### calculate the min and max for plotting after reading each files ###############################
for file in glob.glob(os.path.join(path,'state*.dat')):
	numfile+=1
	#print file
	semiAxis = []
	LongTit = []
	radius = []
	dr = []
	z = []
	minlim=-180
	maxlim=180		
			
		
	with open(file) as f:
		i=0;
		while i<headerline:
			next(f)
			i=i+1
		for line in f:
			parts=line.split()
			semiAxis.append(float(parts[1]))
			radius.append(calc_r(float(parts[1]),float(parts[2]),float(parts[-1])))
			dr.append(calc_dr(float(parts[1]),float(parts[2]),float(parts[-1]),a_ave,e_ave))
			z.append(calc_z(float(parts[1]),float(parts[2]),float(parts[3]),float(parts[5]),float(parts[-1]),float(parts[4])))
		f.close()
	maxSemiAxis = max(maxSemiAxis,max(semiAxis))
	minSemiAxis = min(minSemiAxis,min(semiAxis))
	maxr = max(maxr,max(radius))
	minr = min(minr,min(radius))
	maxdr = max(maxdr,max(dr))
	mindr = min(mindr,min(dr))
	minz = min(minz,min(z))
	maxz = max(maxz,max(z))
	
# chech sign and set limit
if maxSemiAxis == minSemiAxis:
	if maxSemiAxis < 0:
		maxSemiAxis = 0.9*maxSemiAxis
		minSemiAxis = 1.1*minSemiAxis
	elif maxSemiAxis > 0:
		maxSemiAxis = 1.1*maxSemiAxis
		minSemiAxis = 0.9*minSemiAxis
else:
	maxSemiAxis = maxSemiAxis+plotRange*abs(maxSemiAxis-minSemiAxis)
	minSemiAxis = minSemiAxis-plotRange*abs(maxSemiAxis-minSemiAxis)


if maxr == minr and maxz == minz:
	if maxz < 0:
		maxz = 0.9*maxz
		minz = 1.1*minz
	elif maxr > 0:
		maxz = 1.1*maxz
		minz = 0.9*minz
		
	if maxr < 0:
		maxr = 0.9*maxr
		minr = 1.1*minr
	elif maxr > 0:
		maxr = 1.1*maxr
		minr = 0.9*minr	
	

			
elif abs(maxr - minr) < 0.01*abs(maxz-minz):
	maxz = maxz+plotRange*abs(maxz-minz)
	minz = minz-plotRange*abs(maxz-minz)
	maxr = maxr+plotRange*abs(maxz-minz)
	minr = minr-plotRange*abs(maxz-minz)
elif 0.01*abs(maxr - minr) > abs(maxz-minz):
	maxz = maxz+plotRange*abs(maxr-minr)
	minz = minz-plotRange*abs(maxr-minr)
	maxr = maxr+plotRange*abs(maxr-minr)
	minr = minr-plotRange*abs(maxr-minr) 
else:
	maxr = maxr+plotRange*abs(maxr-minr)
 	minr = minr-plotRange*abs(maxr-minr)
	maxz = maxz+plotRange*abs(maxz-minz)
	minz = minz-plotRange*abs(maxz-minz)
	

	
if maxdr == mindr:
	if maxdr < 0:
		maxdr = 0.9*maxdr
		mindr = 1.1*mindr
	elif maxdr > 0:
		maxdr = 1.1*maxdr
		mindr = 0.9*mindr
else:
	maxdr = maxdr+plotRange*abs(maxdr-mindr)
	mindr = mindr-plotRange*abs(maxdr-mindr)


#if maxSemiAxis == minSemiAxis:
#	if maxSemiAxis < 0:
#		maxSemiAxis = 0.9*maxSemiAxis
#		minSemiAxis = 1.1*minSemiAxis
#	elif maxSemiAxis > 0:
#		maxSemiAxis = 1.1*maxSemiAxis
#		minSemiAxis = 0.9*minSemiAxis
#else:
#	maxSemiAxis = maxSemiAxis+0.25*abs(maxSemiAxis-minSemiAxis)
#	minSemiAxis = minSemiAxis-0.25*abs(maxSemiAxis-minSemiAxis)
#
#if maxr == minr:
#	if maxr < 0:
#		maxr = 0.9*maxr
#		minr = 1.1*minr
#	elif maxr > 0:
#		maxr = 1.1*maxr
#		minr = 0.9*minr
#else:
#	maxr = maxr+0.1*abs(maxr-minr)
#	minr = minr-abs(maxr-minr)
#	
#if maxdr == mindr:
#	if maxdr < 0:
#		maxdr = 0.9*maxdr
#		mindr = 1.1*mindr
#	elif maxdr > 0:
#		maxdr = 1.1*maxdr
#		mindr = 0.9*mindr
#else:
#	maxdr = maxdr+0.25*abs(maxdr-mindr)
#	mindr = mindr-0.25*abs(maxdr-mindr)
#
#if maxz == minz:
#	if maxz < 0:
#		maxz = 0.9*maxz
#		minz = 1.1*minz
#	elif maxr > 0:
#		maxz = 1.1*maxz
#		minz = 0.9*minz
#else:
#	maxz = maxz+0.25*abs(maxz-minz)
#	minz = minz-0.25*abs(maxz-minz)

print "finished calculating min and max"	
####### make each state file into png files ###############################
print "Number of files to process is: " +str(numfile)
countnum=0	
			
for file in glob.glob(os.path.join(path,'state*.dat')):
	countnum+=1
	print str(int(float(countnum)/numfile*100))+"% done"
	semiAxis = []
	LongTit = []
	radius = []
	dr = []
	z = []
	name = file.split('/')
	PNGName = str(name[-1])
	#print PNGName
	#print name
	minlim=-180
	maxlim=180		
			
		
	with open(file) as f:
		i=0;
		while i<headerline:
			next(f)
			i=i+1
		for line in f:
			parts=line.split()
			semiAxis.append(float(parts[1]))
			angleCalc = float(parts[-2])+float(parts[-3])
			LongTit.append(angleCalc)
			
			radius.append(calc_r(float(parts[1]),float(parts[2]),float(parts[-1])))
			dr.append(calc_dr(float(parts[1]),float(parts[2]),float(parts[-1]),a_ave,e_ave))
			z.append(calc_z(float(parts[1]),float(parts[2]),float(parts[3]),float(parts[5]),float(parts[-1]),float(parts[4])))
		f.close()

	if int(sys.argv[2])==0:
		LongTit2=[(center_angle(i,-180.,180.)) for i in LongTit]
	elif int(sys.argv[2])==1:
		LongTit2=[(center_angle(i-LongTit[0],-180.,180.)) for i in LongTit]
	else:
		print "input for rotating/non-rotating frame must be 0 or 1"
		sys.exit(1)
		
	### create polar plots	
	if int(sys.argv[3])==1:
	############## plot and save ###############################
	#	RotLong = center_array(np.asarray(LongTit),0,360)
		LongTit_up = []
		LongTit_down = []
		radius_up = []
		radius_down = []
		z_up = []
		z_down = []
		
		for i in range(len(LongTit2)):
			if z[i] > 0:
				LongTit_up.append(LongTit2[i])
				radius_up.append(radius[i])
				z_up.append(z[i])
			else:
				LongTit_down.append(LongTit2[i])
				radius_down.append(radius[i])
				z_down.append(z[i])
	
		fig1 = plt.figure(figsize=(12,10))
		ax1 = plt.subplot(2,2,1, projection='polar')
		ax1.set_title('r top view [planet radii]')
		ax1.set_ylim([minr, maxr])
		ax1.plot(np.array(LongTit_up)*d2r,radius_up,'ro',np.array(LongTit_down)*d2r,radius_down,'bo')
		#ax1.set_ylabel('r top view [planet radii]')
		#ax1.plot(np.array(LongTit2)*d2r,radius)
	
		ax2 = plt.subplot(2,2,4)

		ax2.plot(LongTit_up,z_up,'ro',LongTit_down,z_down,'bo')
		if int(sys.argv[2])==0:
			ax2.set_xlabel('Non-Rotating Longtitude [degrees]')
		elif int(sys.argv[2])==1:
			ax2.set_xlabel('Rotating Longtitude [degrees]')
		ax2.set_ylabel('z [planet radii]')
		ax2.set_xlim([-180,180])
		ax2.set_ylim([minz,maxz])
	
		ax3 = plt.subplot(2,2,3, projection='polar')
		ax3.set_title('z polar plot [planet radii]')
		ax3.set_ylim([minz, maxz])
		ax3.plot(np.array(LongTit_up)*d2r,z_up,'ro',np.array(LongTit_down)*d2r,z_down,'bo')
		#ax3.set_ylabel('z polar plot [planet radii]')
		#ax1.plot(np.array(LongTit2)*d2r,radius)
	
		ax4 = plt.subplot(2,2,2)
		ax4.plot(LongTit_up,radius_up,'ro',LongTit_down,radius_down,'bo')
		if int(sys.argv[2])==0:
			ax4.set_xlabel('Non-Rotating Longtitude [degrees]')
		elif int(sys.argv[2])==1:
			ax4.set_xlabel('Rotating Longtitude [degrees]')
		ax4.set_ylabel('r [planet radii]')
		ax4.set_xlim([-180,180])
		ax4.set_ylim([minr,maxr])
	
	
		timeparts=str(float(parts[0]))
		#print timeparts
		timeprint=[]
		k=0
		for i in range(len(timeparts)+int(printdes)):
			if timeparts[i]=='.':
				timeprint.append(timeparts[i])
				k+=1
			else:
				if k==1:
					if printdes > len(timeparts)-i:
						timeparts=timeparts+'0'*printdes
						#print timeparts
					while k < printdes+1:
						#print(timeparts[i])
						timeprint.append(timeparts[i])
						k+=1
						i+=1
					break
				else:
					timeprint.append(timeparts[i])
				
		#print timeprint	
		timeprint=''.join(map(str, timeprint))	
	
		if int(sys.argv[2])==0:
			plt.suptitle('Non-Rotating Frame, Time: '+ int(10-len(timeprint))*" "+ timeprint)
		elif int(sys.argv[2])==1:
			plt.suptitle('Rotating Frame, Time: '+ int(10-len(timeprint))*" "+ timeprint)
		plt.savefig(PNGName+'.png')
		plt.close()
	#### create linear plot	
	elif int(sys.argv[3])==0:
		############## plot and save ###############################
		plt.figure(figsize=(10, 10))
	
		# sort axis
		LongTit_semi,semiAxis = zip(*sorted(zip(LongTit2, semiAxis)))
		LongTit_r,radius = zip(*sorted(zip(LongTit2, radius)))
		LongTit_dr,dr = zip(*sorted(zip(LongTit2, dr)))
		LongTit_z,z = zip(*sorted(zip(LongTit2, z)))
	
		# semimajor axis
		plt.subplot(2,2,1)
		plt.plot(LongTit_semi,semiAxis,'-o')
		if int(sys.argv[2])==0:
			plt.xlabel('Non-Rotating Longtitude [degrees]')
		elif int(sys.argv[2])==1:
			plt.xlabel('Rotating Longtitude [degrees]')
		plt.ylabel('Semi-major Axis [planet radii]')
		plt.ylim([minSemiAxis, maxSemiAxis])
		plt.xlim([minlim,maxlim])
	
	
		# radius
		plt.subplot(2,2,2)
		plt.plot(LongTit_r,radius,'-o')
		if int(sys.argv[2])==0:
			plt.xlabel('Non-Rotating Longtitude [degrees]')
		elif int(sys.argv[2])==1:
			plt.xlabel('Rotating Longtitude [degrees]')
		plt.ylabel('r [planet radii]')
		plt.ylim([minr, maxr])
		plt.xlim([minlim,maxlim])
	
		# dr
		plt.subplot(2,2,3)
		plt.plot(LongTit_dr,dr,'-o')
		if int(sys.argv[2])==0:
			plt.xlabel('Non-Rotating Longtitude [degrees]')
		elif int(sys.argv[2])==1:
			plt.xlabel('Rotating Longtitude [degrees]')
		plt.ylabel('dr [planet radii]')
		plt.ylim([mindr, maxdr])
		plt.xlim([minlim,maxlim])
	
		# z
		plt.subplot(2,2,4)
		plt.plot(LongTit_z,z,'-o')
		if int(sys.argv[2])==0:
			plt.xlabel('Non-Rotating Longtitude [degrees]')
		elif int(sys.argv[2])==1:
			plt.xlabel('Rotating Longtitude [degrees]')
		plt.ylabel('z [planet radii]')
		plt.ylim([minz, maxz])
		plt.xlim([minlim,maxlim])
	
		timeparts=str(float(parts[0]))
		#print timeparts
		timeprint=[]
		k=0
		for i in range(len(timeparts)+int(printdes)):
			if timeparts[i]=='.':
				timeprint.append(timeparts[i])
				k+=1
			else:
				if k==1:
					if printdes > len(timeparts)-i:
						timeparts=timeparts+'0'*printdes
						#print timeparts
					while k < printdes+1:
						#print(timeparts[i])
						timeprint.append(timeparts[i])
						k+=1
						i+=1
					break
				else:
					timeprint.append(timeparts[i])
				
		#print timeprint	
		timeprint=''.join(map(str, timeprint))	
		#print timeparts
		if int(sys.argv[2])==0:
			plt.suptitle('Non-Rotating Frame, Time: '+ int(10-len(timeprint))*" "+ timeprint)
		elif int(sys.argv[2])==1:
			plt.suptitle('Rotating Frame, Time: '+ int(10-len(timeprint))*" "+ timeprint)
		plt.savefig(str(path)+"/pngfiles/"+PNGName+'.png')
		plt.close()

	else:
		print "input for linear/polar plot must be 0 or 1"
		sys.exit(1)
FolderName=path.split('/')
if FolderName[-1]=='.':
	#print("ffmpeg -framerate 10 -i "+ str(path)+"/pngfiles/"+"state%d.dat.png -loglevel warning -pix_fmt yuv420p -y "+NameRotNRot[int(sys.argv[2])]+"_"+NameLinPol[int(sys.argv[3])]+".mp4")
	os.system("ffmpeg -framerate 10 -i "+str(path)+"/pngfiles/"+"state%d.dat.png -loglevel warning -pix_fmt yuv420p -y " + NameRotNRot[int(sys.argv[2])] + "_" + NameLinPol[int(sys.argv[3])] + ".mp4")
	#print 1
else:
	os.system("ffmpeg -framerate 10 -i "+ str(path)+"/pngfiles/state%d.dat.png -loglevel warning -pix_fmt yuv420p -y "+FolderName[-1]+"_"+NameRotNRot[int(sys.argv[2])]+"_"+NameLinPol[int(sys.argv[3])]+".mp4")
	os.system("mv "+FolderName[-1]+"_"+NameRotNRot[int(sys.argv[2])]+"_"+NameLinPol[int(sys.argv[3])]+".mp4 "+str(path))

#print path
#print "mv "+FolderName[-1]+"_"+NameRotNRot[int(sys.argv[2])]+"_"+NameLinPol[int(sys.argv[3])]+".mp4 "+str(path)
#print "mkdir "+str(path)+"/pngfiles"
#print "mv state*.dat.png" + str(path)+"/pngfiles"
#os.system("mv "+FolderName[-1]+"_"+NameRotNRot[int(sys.argv[2])]+"_"+NameLinPol[int(sys.argv[3])]+".mp4 "+str(path))		
#os.system("mv state*.dat.png " + str(path)+"/pngfiles")
os.system("rm -rf "+str(path)+"/pngfiles")
