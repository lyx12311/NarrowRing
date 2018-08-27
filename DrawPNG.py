#!/usr/bin/env python
import numpy as np
import math
import os
import matplotlib.pyplot as plt
import sys 
import glob
from math import log10, floor
from decimal import *
from getEle import *
from hnread import *
from chkEle import *
from center_angle import *
from TimeGenerate import *

d2r = 0.01745329251
r2d = 57.2957795131
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

# check error
checkinput(sys.argv)



path=sys.argv[1] ## put second input into file 
pathname=str(path)
if pathname[-1]=="/":
	path=pathname[0:-1]

os.system("mkdir "+path+"/pngfiles")
print "mkdir "+path+"/pngfiles"

####### calculates the reference semimajor axis and eccentricity from first state file
radiusfirstfile=[]
zfirstfile = []

# count and sort files
filename=[]
filenumb=[]
for file in glob.glob(os.path.join(path,'state*.dat')):
	filename_one =(file.split('/'))[-1]
	filename.append(str(file))
	filenumb.append(filename_one.split('e')[-1].split('.')[-2])

filenumb, filename = zip(*sorted(zip([int(i) for i in filenumb],filename)))
print "first file to read is: state"+str(filenumb[0])+".dat"

a = getEle(filename[0],'a')
e = getEle(filename[0],'e')
cw = getEle(filename[0],'cw')
nu = getEle(filename[0],'nu')
i = getEle(filename[0],'i')
W = getEle(filename[0],'W')

radiusfirstfile = a*(1.-e*e)/(1.+e*np.cos(nu*d2r))
zfirstfile = a*(1.-e*e)/(1.+e*np.cos(nu*d2r))*np.sin(i*d2r)*np.sin((cw-W+nu)*d2r)

a_ave=np.mean(a)
e_ave=np.mean(getEle(filename[0],'e'))
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
for file in filename:
	semiAxis = getEle(file,'a')
	e = getEle(file,'e')
	cw = getEle(file,'cw')
	nu = getEle(file,'nu')
	i = getEle(file,'i')
	W = getEle(file,'W')

	radius = a*(1.-e*e)/(1.+e*np.cos(nu*d2r))
	z = a*(1.-e*e)/(1.+e*np.cos(nu*d2r))*np.sin(i*d2r)*np.sin((cw-W+nu)*d2r)
	dr = a*(1.-e*e)/(1.+e*np.cos(nu*d2r))-a_ave*(1.-e_ave*e_ave)/(1.+e_ave*np.cos(nu*d2r))

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


print "finished calculating min and max"	
####### make each state file into png files ###############################
print "Number of files to process is: " +str(len(filenumb))
countnum=0				
for file in glob.glob(os.path.join(path,'state*.dat')):
	countnum+=1
	if int(float(countnum)/len(filenumb)*100)-int(float(countnum-1)/len(filenumb)*100)!=0:
		print str(int(float(countnum)/len(filenumb)*100))+"% done"
	name = file.split('/')
	PNGName = str(name[-1])
	minlim=-180
	maxlim=180		
			
	
	semiAxis = getEle(file,'a')
	cw = getEle(file,'cw')
	LongTit = cw+getEle(file,'M')
	e = getEle(file,'e')
	nu = getEle(file,'nu')
	i = getEle(file,'i')
	W = getEle(file,'W')
	t = getEle(file,'t')
	
	radius = semiAxis*(1.-e*e)/(1.+e*np.cos(nu*d2r))
	z = semiAxis*(1.-e*e)/(1.+e*np.cos(nu*d2r))*np.sin(i*d2r)*np.sin((cw-W+nu)*d2r)
	
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
	
		ax4 = plt.subplot(2,2,2)
		ax4.plot(LongTit_up,radius_up,'ro',LongTit_down,radius_down,'bo')
		if int(sys.argv[2])==0:
			ax4.set_xlabel('Non-Rotating Longtitude [degrees]')
		elif int(sys.argv[2])==1:
			ax4.set_xlabel('Rotating Longtitude [degrees]')
		ax4.set_ylabel('r [planet radii]')
		ax4.set_xlim([-180,180])
		ax4.set_ylim([minr,maxr])
	
		if int(sys.argv[2])==0:
			plt.suptitle('Non-Rotating Frame, Time: '+ TimeGenerate(t[0],4,10))
		elif int(sys.argv[2])==1:
			plt.suptitle('Rotating Frame, Time: '+ TimeGenerate(t[0],4,10))
		plt.savefig(str(path)+"/pngfiles/"+PNGName+'.png')
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
	
		if int(sys.argv[2])==0:
			plt.suptitle('Non-Rotating Frame, Time: '+ TimeGenerate(t[0],4,10))
		elif int(sys.argv[2])==1:
			plt.suptitle('Rotating Frame, Time: '+ TimeGenerate(t[0],4,10))
		plt.savefig(str(path)+"/pngfiles/"+PNGName+'.png')
		plt.close()

	else:
		print "input for linear/polar plot must be 0 or 1"
		sys.exit(1)
FolderName=path.split('/')
if FolderName[-1]=='.':
	os.system("ffmpeg -framerate 10 -i "+str(path)+"/pngfiles/"+"state%d.dat.png -loglevel warning -pix_fmt yuv420p -y " + NameRotNRot[int(sys.argv[2])] + "_" + NameLinPol[int(sys.argv[3])] + ".mp4")
else:
	os.system("ffmpeg -framerate 10 -i "+ str(path)+"/pngfiles/state%d.dat.png -loglevel warning -pix_fmt yuv420p -y "+FolderName[-1]+"_"+NameRotNRot[int(sys.argv[2])]+"_"+NameLinPol[int(sys.argv[3])]+".mp4")
	os.system("mv "+FolderName[-1]+"_"+NameRotNRot[int(sys.argv[2])]+"_"+NameLinPol[int(sys.argv[3])]+".mp4 "+str(path))

os.system("rm -rf "+str(path)+"/pngfiles")
