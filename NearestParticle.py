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
import scipy.fftpack
from hnread import *
from center_angle import *
d2r = 0.01745329251
r2d = 57.2957795131

# check command line arguments 
def checkinput(argv):                                                                       
    programname = sys.argv[0]                                                               
    if len(argv) != 4:  # Exit if not exactly one arguments  
    	print '---------------------------------------------------------------------------'                               
        print 'This program plots relationship between the distance between two particles, it takes into the hnbody run folder and plotting particle numbers as argument.\n '
	print ' '
	print ' Example:    '+programname+' ./ 3 2' 
	print '---------------------------------------------------------------------------'                                    
        sys.exit(1)                                                                         
    gridfile = argv[1]                                                                                                                                    
    if not os.path.isdir(gridfile):  # Exit if folder does not exist                  
        print 'ERROR: unable to locate folder ' + gridfile                             
        sys.exit(1)                                                                            
checkinput(sys.argv)
pathf=sys.argv[1] ## put second input into file 

upPart=max([int(i) for i in [sys.argv[2],sys.argv[3]]])
bottomPart=min([int(i) for i in [sys.argv[2],sys.argv[3]]])
#print upPart
#print bottomPart
pathname=str(pathf)
#print pathnames
if pathname[-1]=="/":
	pathf=pathname[0:-1]

positiondiff=[]
avePositiondiff=[]
t=[]
inte=0
for file in glob.glob(os.path.join(pathf,'state*.dat')):
	data=hnread(file,"state")
	LongTit = [center_angle(i,-180,180) for i in (data[:,-2]+data[:,-3])]
	positiondiff.append(center_angle(LongTit[upPart-1]-LongTit[bottomPart-1],-180,180))
	#print center_angle(LongTit[upPart-1]-LongTit[bottomPart-1],-180,180)
	#print LongTit[upPart-1]
	#print LongTit[bottomPart-1]
	avePositiondiff.append(np.mean([center_angle(LongTit[i+1]-LongTit[i],-180,180) for i in range(len(LongTit)-1)]))
	t.append(data[0,0])
	if inte==0:	
		initialDiff=center_angle(LongTit[upPart-1]-LongTit[bottomPart-1],-180,180)
		initialDiffAve=np.mean([center_angle(LongTit[i+1]-LongTit[i],-180,180) for i in range(len(LongTit)-1)])
	inte=inte+1

t, positiondiff, avePositiondiff = zip(*sorted(zip(t, positiondiff, avePositiondiff)))
#positiondiff=[(i-initialDiff) for i in positiondiff]

#t_fft=t[0:int(len(t)/2.)]
#positiondiff_fft=positiondiff[0:int(len(t)/2.)]
t_fft=t
positiondiff_fft=positiondiff


# do fft
tmin=min(t_fft)
tmax=max(t_fft)
Fs=200000.
Ts=(tmax-tmin)/Fs
t_int=np.linspace(tmin,tmax,Fs) # time vector
n = len(positiondiff_fft) # length of the signal
Y=np.fft.fft(positiondiff_fft)
Y = 2./n*abs(Y[0:n/2])
frq=np.linspace(tmin/(2.*Ts),tmax/(2.*Ts),int(n/2))

rangeDiff=max(positiondiff)-min(positiondiff)
toplim=(np.mean(avePositiondiff))-0.6*rangeDiff
bottomlim=(np.mean(avePositiondiff))+0.6*rangeDiff
if np.std(avePositiondiff) < (bottomlim-toplim)/2:
	plt.figure()
	plt.subplot(411)
	plt.plot(t,positiondiff,'-o')
	plt.title('Longt diff for particle '+ str(upPart-1) + ' and particle ' + str(bottomPart-1))
	plt.xlabel('Time [yr]')
	plt.ylabel('Longt diff [degrees]')
	plt.ylim([min(positiondiff)-0.1*rangeDiff,max(positiondiff)+0.1*rangeDiff])

	plt.subplot(412)
	plt.semilogy(frq,abs(Y))
	plt.title('FFT of '+'Longt diff for particle '+ str(upPart-1) + ' and particle ' + str(bottomPart-1))
	plt.xlabel('Frequency [1/yr]')
	plt.ylabel('|Y(freq)|')
	#fftrange=max(abs(Y))-min(abs(Y))
	#toplim=(min(abs(Y)))-0.1*fftrange
	#bottomlim=(max(abs(Y)))+0.1*fftrange
	#plt.ylim([toplim,bottomlim])
	plt.ylim([-0.001,1])

	plt.subplot(413)
	plt.plot(t,avePositiondiff,'-o')
	plt.title('Avereage longtitude difference')
	plt.xlabel('Time [yr]')
	plt.ylabel('Longt diff [degrees]')
	plt.ylim([toplim,bottomlim])

	plt.subplot(414)
	plt.plot(t,avePositiondiff,'-o')
	plt.xlabel('Time [yr]')
	plt.ylabel('Longt diff [degrees]')

else:
	plt.figure()
	plt.subplot(311)
	plt.plot(t,positiondiff,'-o')
	plt.title('Longt diff for particle '+ str(upPart-1) + ' and particle ' + str(bottomPart-1))
	plt.xlabel('Time [yr]')
	plt.ylabel('Longt diff [degrees]')
	plt.ylim([min(positiondiff)-0.1*rangeDiff,max(positiondiff)+0.1*rangeDiff])

	plt.subplot(312)
	plt.semilogy(frq,abs(Y))
	#plt.plot(frq,abs(Y))
	plt.title('FFT of '+'Longtitude difference for particle '+ str(upPart-1) + ' and particle ' + str(bottomPart-1))
	plt.xlabel('Frequency [1/yr]')
	plt.ylabel('|Y(freq)|')
	#fftrange=max(abs(Y))-min(abs(Y))
	#toplimfft=(min(abs(Y)))-0.1*fftrange
	#bottomlimfft=(max(abs(Y)))+0.1*fftrange
	#plt.ylim([toplimfft,bottomlimfft])
	plt.ylim([-0.001,0.8])

	plt.subplot(313)
	plt.plot(t,avePositiondiff,'-o')
	plt.title('Avereage longtitude difference')
	plt.xlabel('Time [yr]')
	plt.ylabel('Longt diff [degrees]')
	#plt.ylim([toplim,bottomlim])
	plt.tight_layout()
		
plt.savefig(pathf+"/NearestParticleDis"+str(bottomPart)+str(upPart)+".png")   


plt.show()
