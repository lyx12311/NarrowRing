#!/usr/bin/env python
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
from hnhelper import *


d2r = 0.01745329251
r2d = 57.2957795131

GM =  171982516.97368595#5.683e26*6.67e-11 #first line of body file

def checkinput(argv):                                                                       
    programname = sys.argv[0]                                                               
    if len(argv) != 3:  # Exit if not exactly one arguments  
        print '---------------------------------------------------------------------------'                               
        print "This program converts input file from stream.pl with J2.\n It takes into the input file name and output file name as arguments"
        print ' '
        print ' Example:    '+programname+' M.in M_J2.in'  
        print '---------------------------------------------------------------------------'                                    
        sys.exit(1)                                                                                                                                                                                                            

checkinput(sys.argv)

filename=sys.argv[1]
fileout=sys.argv[2]

def MconvHn(filename):
	fw=open("tempM.in","w")
	fw.write("462639 301 0 171982516.97368595 156816351.27765289 1\n")
	fw.write("0 1.0000000000000001e-05 20000 8 18\n")
	fw.write("0 21 7  8  9  10 12 15\n")
	fw.write("#\n")
	fw.write("# HNBody system state file (Bodycentric coordinates).\n")
	fw.write("#\n")
	fw.write("# Line 3 encodes the data type for each column as follows:\n")
	fw.write("#\n")
	fw.write("#  0-Time (= Epoch)  1-x1 2-x2 3-x3   4-v1 5-v2 6-v3\n")
	fw.write("#  7-SemiMajorAxis   8-Eccentricity   9-Inclination\n")
	fw.write("# 10-LongAscendNode 11-ArgPeriapse   12-LongPeriapse\n")
	fw.write("# 13-TimePeriapse   14-PeriDistance  15-MeanAnomaly\n")
	fw.write("# 16-TrueAnomaly    17-MeanLongitude 18-TrueLongitude\n")
	fw.write("# 19-MeanLatitude   20-TrueLatitude  21-Mass\n")
	fw.write("# 22-EncRadius      23-CaptRadius    24-IdTag\n")
	fw.write("# 25-JacIndex       26-StepMult\n")
	fw.write("#\n")
	
	with open(filename) as f:
		parts=f.readlines()
		for lines in parts[5:len(parts)]:
			fw.write("0.0   "+lines.split("#")[0]+"\n")
		return parts[0:5]
	
	fw.close()
		
headert=MconvHn(filename)
tempF="tempM.in"
Rp,J2=hnread("input.hnb","input")

# calculate frequencies
def calcK(GM,a,Rp,J2):
	return np.sqrt(GM/np.power(a,3.))*(1.-3./4.*np.power((1/a),2)*J2)

def calcN(GM,a,Rp,J2):
	return np.sqrt(GM/np.power(a,3.))*(1.+9./4.*np.power((1/a),2)*J2)
	
def calcX2(GM,a,Rp,J2):
	return GM/np.power(a,3.)*(1.+15./2.*np.power((1/a),2)*J2)

def Calc_Omega(GM,a,Rp,J2):
	return np.sqrt(GM/np.power(a,3.))*(1.+3./4.*np.power((1/a),2)*J2)

# caculate r, theta, z and drdt, dthetadt, dzdt (inputs are degrees)
def calc_re(a,e,M):
	M=M*d2r
	return a*(1.-e*np.cos(M))
	
def calc_ze(a,i,w,M):
	M=M*d2r
	i=i*d2r
	w=w*d2r
	return a*i*np.sin(w+M)

def calc_thetae(cw,M,Omega,K,e):
	M=M*d2r
	cw=cw*d2r
	return cw+M+2.*Omega/K*e*np.sin(M)

def calc_drdt(a,K,e,M):
	M=M*d2r
	return a*K*e*np.sin(M)
	
def calc_dzdt(a,i,N,w,M):
	M=M*d2r
	w=w*d2r
	i=i*d2r
	return a*i*N*(np.cos(w+M))
	
def calc_dthetadt(Omega,e,M):
	M=M*d2r
	return (1.+2.*e*np.cos(M))*Omega

# inputs are radians
def getx(r,theta):
	return r*np.cos(theta)

def gety(r,theta):
	return r*np.sin(theta)
	
def getvx(r,theta,drdt,dthetadt):
	return drdt*np.cos(theta)-r*dthetadt*np.sin(theta)

def getvy(r,theta,drdt,dthetadt):
	return drdt*np.sin(theta)+r*dthetadt*np.cos(theta)

# start writing to files
fw=open(fileout,"w")
fw.write("#462639 301 0 171982516.97368595 156816351.27765289 1\n")
fw.write("#0 1.0000000000000001e-05 20000 8 18\n")
fw.write("#0 21 1 2 3 4 5 6\n")
fw.write("#\n")
fw.write("# HNBody system state file (Bodycentric coordinates).\n")
fw.write("#\n")
fw.write("# Line 3 encodes the data type for each column as follows:\n")
fw.write("#\n")
fw.write("#  0-Time (= Epoch)  1-x1 2-x2 3-x3   4-v1 5-v2 6-v3\n")
fw.write("#  7-SemiMajorAxis   8-Eccentricity   9-Inclination\n")
fw.write("# 10-LongAscendNode 11-ArgPeriapse   12-LongPeriapse\n")
fw.write("# 13-TimePeriapse   14-PeriDistance  15-MeanAnomaly\n")
fw.write("# 16-TrueAnomaly    17-MeanLongitude 18-TrueLongitude\n")
fw.write("# 19-MeanLatitude   20-TrueLatitude  21-Mass\n")
fw.write("# 22-EncRadius      23-CaptRadius    24-IdTag\n")
fw.write("# 25-JacIndex       26-StepMult\n")
fw.write("#\n")
	
a=getEle(tempF,"a")
e=getEle(tempF,"e") 
I=getEle(tempF,"i")
M=getEle(tempF,"M")
w=getEle(tempF,"w")
cw=getEle(tempF,"cw")
Mass=getEle(tempF,"mass")
for i in range(len(a)):

	Omega=Calc_Omega(GM,a[i],Rp,J2)
	K=calcK(GM,a[i],Rp,J2)
	N=calcN(GM,a[i],Rp,J2)
	X2=calcX2(GM,a[i],Rp,J2)
	
	r=calc_re(a[i],e[i],M[i])
	theta=calc_thetae(cw[i],M[i],Omega,K,e[i])
	#print(theta)
	drdt=calc_drdt(a[i],K,e[i],M[i])
	dthetadt=calc_dthetadt(Omega,e[i],M[i])
	
	mass=Mass[i]
	x=getx(r,theta)
	y=gety(r,theta)
	z=calc_ze(a[i],I[i],w[i],M[i])
	
	vx=getvx(r,theta,drdt,dthetadt)
	vy=getvy(r,theta,drdt,dthetadt)
	vz=calc_dzdt(a[i],I[i],N,w[i],M[i])
	
	fw.write(str(mass)+" "+str(x)+" "+str(y)+" "+str(z)+" "+str(vx)+" "+str(vy)+" "+str(vz)+"\n")
print("J2 is: "+str(J2))

os.system("rm -rf tempM.in")
