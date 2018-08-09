#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Author: Lucy Lu (last update 08/08/2018)
# Contain functions: 
#	unevenfft(filename,Fs,N) [uneven fft for state files]
#		filename: file path
#		Fs: pow many points to sample
#		N: number of peaks to find
#		dub: how many times to duplicate data 
#		opt: print out option (whether to print out highest peak amplitude (1) or not (0))
#			example: unevenfft("state1.dat",1000,3,1) returns a plot marking the first 3 highest peaks and print out the amplitude
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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
from TimeGenerate import *
# this function does uneven fft for state files
# filename: file name 
# Fs: pow many points to sample
# N: number of peaks to find
def unevenfft(filename,Fs,N,dub,opt):
	data=hnread(filename,"state")
	longtit=data[:,-3]+data[:,-2]
	#print sorted(longtit)
	longtit_center=np.array([center_angle(i,0,360) for i in longtit])
	longtit_or=longtit_center
	
	r=[calc_r(data[i,1],data[i,2],data[i,-1]) for i in range(len(longtit))]
	r_or=r
	#r=np.cos(5*np.pi*longtit_center/2)
	#r=np.sin(2*np.pi*5.*np.array(longtit_center)/100)
	
	t=data[0,0]
	
	longtit_center, r = zip(*sorted(zip(longtit_center, r)))
	
	longtit_center=list(longtit_center)
	r=list(r)
	
	#print len(longtit_center)
	#print len(r)
	
	for i in range(dub):
		for j in longtit_or:
			longtit_center.append(j+(i+1)*360)
		for k in r_or:
			r.append(k)
	
	
	
	longtit_center, r = zip(*sorted(zip(longtit_center, r)))
	
	#plt.plot(longtit_center,r)
	#plt.show()
	
	
	longtit_center=np.array(longtit_center)
	r=np.array(r)	
	
	if len(longtit)<=3:
		print "Warning: particle number is too small, use larger particle numbers to get better resuls!"
		#print longtit_center
		f2 = interp1d(longtit_center, r, fill_value="extrapolate")
	else:
		#print longtit_center
		f2 = interp1d(longtit_center, r,kind='cubic', fill_value="extrapolate")
	
	
#	tmin=min(longtit_center)
#	tmax=max(longtit_center)
	
	tmin=0.1
	tmax=max(longtit_center)
	
	Ts=(tmax-tmin)/Fs # sample rate
	#print Ts
	t_int=np.linspace(tmin,tmax,Fs) # time vector
	#print len(t_int)
	r_int=f2(t_int)
	
	n = len(r_int) # length of the signal
	Y=np.fft.fft(r_int)
	Y = 2./n*abs(Y[0:n/2])
	frq=np.linspace(0,tmax/(2.*Ts),int(n/2))
	
	sortedY,sortedFre=zip(*sorted(zip(abs(Y),frq)))
	#print frq
	#print min(frq)
	#print len(sortedY)
	#print sortedY
	
	titlefre='Peaks are at frequency:'
	fren=[]
	#print sortedY
	
	# calculate mean and std of background noise
	bgn=np.mean(sortedY[0:int(3*len(sortedY)/4)])
	bgn_e=np.std(np.array(sortedY[0:int(2*len(sortedY)/3)]))
	Nc=N
	#print bgn
	#print bgn_e
	#print sortedY
	i=0
	while i < Nc:
		#print i
		if sortedY[int(-2-i)] > bgn+100*bgn_e:
			if len(fren)==0:
				titlefre=titlefre+" "+str(int((sortedFre[int(-2-i)])/float(dub+1)))
				fren.append(sortedFre[int(-2-i)]/float(dub+1))
				i=i+1
				
			elif sum( [int((sortedFre[int(-2-i)])/float(dub+1))==int(j) for j in fren])==0:
				titlefre=titlefre+" "+str(int((sortedFre[int(-2-i)])/float(dub+1)))
				fren.append(sortedFre[int(-2-i)]/float(dub+1))
				i=i+1
			else:
				Nc=Nc+1
				i=i+1

	titlefre=titlefre+" in decreasing amplitude order"
	
	printtxt=" "
	peakInt=" "
	for num in range(N):
		printtxt=printtxt+str(sortedY[-int(N+1)+num])+" "
	
	for num in range(N):
		peakInt=peakInt+str(sortedFre[-int(N+1)+num]/float(dub+1))+" "
	print peakInt
	print printtxt
	
	fren.sort()
	
	fig, ax = plt.subplots(2, 1,figsize=(10,6))
	ax[0].plot(longtit_center,r,'o',t_int,r_int,'-')
	#ax[0].set_ylim([1.996,2.005])
	ax[0].set_xlim([0,360])
	ax[0].set_xlabel('Longtitude [degrees]')
	ax[0].set_ylabel('R [planet radii]')
	ax[0].set_title("Time: "+TimeGenerate(t,4,10))
	ax[1].semilogy(frq/float(dub+1),abs(Y),'r') # plotting the spectrum
	ax[1].plot(np.array(sortedFre[-int(N+1):-1])/float(dub+1),sortedY[-int(N+1):-1],'.')
	
	ax[1].set_title(titlefre)
	
	#ax[1].set_xlim([1,max(frq)/float(dub+1)])
	ax[1].set_xlim([1,50])
	ax[1].set_ylim([1e-10,1e-1])
	ax[1].set_xlabel('Freq (1/degrees)')
	ax[1].set_ylabel('|Y(freq)|')
	fig.tight_layout()
	#plt.savefig(str(filename)+'.png')
	#plt.show()

#unevenfft("state14.dat",1000)
