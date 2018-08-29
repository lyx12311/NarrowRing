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
	z=[calc_z(data[i,1],data[i,2],data[i,3],data[i,5],data[i,-1],data[i,4]) for i in range(len(longtit))]
	r_or=r
	z_or=z
	#r=np.cos(5*np.pi*longtit_center/2)
	#r=np.sin(2*np.pi*5.*np.array(longtit_center)/100)
	
	t=data[0,0]
	
	longtit_center, r, z = zip(*sorted(zip(longtit_center, r, z)))
	
	longtit_center=list(longtit_center)
	r=list(r)
	z=list(z)
	
	#print len(longtit_center)
	#print len(r)
	
	for i in range(dub):
		for j in longtit_or:
			longtit_center.append(j+(i+1)*360)
		for k in r_or:
			r.append(k)
		for l in z_or:
			z.append(l)
	
	
	
	longtit_center, r, z = zip(*sorted(zip(longtit_center, r, z)))
	
	#plt.plot(longtit_center,r)
	#plt.show()
	
	
	longtit_center=np.array(longtit_center)
	r=np.array(r)	
	z=np.array(z)
	
	if len(longtit)<=3:
		print "Warning: particle number is too small, use larger particle numbers to get better resuls!"
		#print longtit_center
		f2 = interp1d(longtit_center, r, fill_value="extrapolate")
		f2z = interp1d(longtit_center, z, fill_value="extrapolate")
	else:
		#print longtit_center
		f2 = interp1d(longtit_center, r,kind='cubic', fill_value="extrapolate")
		f2z = interp1d(longtit_center, z,kind='cubic', fill_value="extrapolate")
	
	
#	tmin=min(longtit_center)
#	tmax=max(longtit_center)
	
	tmin=0.1
	tmax=max(longtit_center)
	
	Ts=(tmax-tmin)/Fs # sample rate
	t_int=np.linspace(tmin,tmax,Fs) # time vector
	r_int=f2(t_int)
	z_int=f2z(t_int)
	
	n = len(r_int) # length of the signal
	Y=np.fft.fft(r_int)
	Y_z=np.fft.fft(z_int)
# phase	####Y_or=Y[0:n/2] 
	Y = 2./n*abs(Y[0:n/2])
	Y_z=2./n*abs(Y_z[0:n/2])
	
# phase	####thred=max(Y)/100.
# phase	####for i in range(len(Y_or)):
# phase	####	if abs(Y_or[i])<thred:
# phase	####		Y_or[i]==0
	
# phase	####PH = [math.atan2(k.imag,k.real) for k in Y_or]
	
	frq=np.linspace(0,tmax/(2.*Ts),int(n/2))
	
# phase	####plt.plot(frq,PH)
# phase	####plt.ylim([-3,3])
# phase	####plt.show()
	
	
	sortedY,sortedFre=zip(*sorted(zip(abs(Y),frq)))
	sortedY_z,sortedFre_z=zip(*sorted(zip(abs(Y_z),frq)))
	titlefre='Peaks are at frequency:'
	titlefre_z='Peaks are at frequency:'
	fren=[]
	fren_z=[]
	
	# calculate mean and std of background noise
	bgn=np.mean(sortedY[0:int(3*len(sortedY)/4)])
	bgn_e=np.std(np.array(sortedY[0:int(2*len(sortedY)/3)]))
	
	bgn_z=np.mean(sortedY_z[0:int(3*len(sortedY_z)/4)])
	bgn_e_z=np.std(np.array(sortedY_z[0:int(2*len(sortedY_z)/3)]))
	
	Nc=N
	#print bgn
	#print bgn_e
	#print sortedY
	i=0
	while i < Nc:
		#print i
		if sortedY[int(-2-i)] > bgn+100*bgn_e:
			if len(fren)==0 and int(sortedFre[int(-2-i)]/float(dub+1))>1:
				titlefre=titlefre+" "+str(int((sortedFre[int(-2-i)])/float(dub+1)))
				fren.append(sortedFre[int(-2-i)]/float(dub+1))
				i=i+1
				
			elif sum( [int((sortedFre[int(-2-i)])/float(dub+1))==int(j) for j in fren])==0 and int(sortedFre[int(-2-i)]/float(dub+1))>1:
				titlefre=titlefre+" "+str(int((sortedFre[int(-2-i)])/float(dub+1)))
				fren.append(sortedFre[int(-2-i)]/float(dub+1))
				i=i+1
			else:
				Nc=Nc+1
				i=i+1
				
		else:
			break
	
	# for z
	i=0
	while i < Nc:
		#print i
		if sortedY_z[int(-2-i)] > bgn_z+100*bgn_e_z:
			if len(fren_z)==0 and int(sortedFre_z[int(-2-i)]/float(dub+1))>1:
				titlefre_z=titlefre_z+" "+str(int((sortedFre_z[int(-2-i)])/float(dub+1)))
				fren_z.append(sortedFre_z[int(-2-i)]/float(dub+1))
				i=i+1
				
			elif sum( [int((sortedFre_z[int(-2-i)])/float(dub+1))==int(j) for j in fren_z])==0 and int(sortedFre_z[int(-2-i)]/float(dub+1))>1:
				titlefre_z=titlefre_z+" "+str(int((sortedFre_z[int(-2-i)])/float(dub+1)))
				fren_z.append(sortedFre_z[int(-2-i)]/float(dub+1))
				i=i+1
			else:
				Nc=Nc+1
				i=i+1
				
		else:
			break

	titlefre=titlefre+" in decreasing amplitude order"
	titlefre_z=titlefre_z+" in decreasing amplitude order"
	#print "title done"
	# only printing radial peaks
	printtxt=" "
	peakInt=" "
	for num in range(N):
		printtxt=printtxt+str(sortedY[-int(N+1)+num])+" "
	
	for num in range(N):
		peakInt=peakInt+str(sortedFre[-int(N+1)+num]/float(dub+1))+" "
	if opt!=0:
		print peakInt
		print printtxt
	
	
	fig, ax = plt.subplots(4, 1,figsize=(9,11))
	ax[0].plot(longtit_center,r,'o',t_int,r_int,'-')
	ax[0].set_xlim([0,360])
	ax[0].set_xlabel('Longtitude [degrees]')
	ax[0].set_ylabel('R [planet radii]')
	ax[0].set_title("Time: "+TimeGenerate(t,4,10))
	
	ax[1].semilogy(frq/float(dub+1),abs(Y),'r') # plotting the spectrum
	ax[1].plot(np.array(sortedFre[-int(N+1):-1])/float(dub+1),sortedY[-int(N+1):-1],'.')
	ax[1].set_title(titlefre)
	ax[1].set_xlim([1,max(frq)/float(dub+1)])
	ax[1].set_ylim([1e-10,1e-1])
	ax[1].set_xlabel('Freq (1/degrees)')
	ax[1].set_ylabel('|Y(freq)|')
	
	ax[2].plot(longtit_center,z,'o',t_int,z_int,'-')
	ax[2].set_xlim([0,360])
	ax[2].set_xlabel('Longtitude [degrees]')
	ax[2].set_ylabel('Z [planet radii]')
	
	ax[3].semilogy(frq/float(dub+1),abs(Y_z),'r') # plotting the spectrum
	ax[3].plot(np.array(sortedFre_z[-int(N+1):-1])/float(dub+1),sortedY_z[-int(N+1):-1],'.')
	ax[3].set_title(titlefre_z)
	ax[3].set_xlim([1,max(frq)/float(dub+1)])
	ax[3].set_ylim([1e-11,1e-6])
	ax[3].set_xlim([1,max(frq)/float(dub+1)])
	ax[3].set_xlabel('Freq (1/degrees)')
	ax[3].set_ylabel('|Y_z(freq)|')
	
	#fig.tight_layout()

#unevenfft("state14.dat",1000)
