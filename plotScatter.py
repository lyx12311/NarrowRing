#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Author: Lucy Lu (last update 08/03/2018)
# Contain functions: 
#	plotScatter(ColorCVariable,x,y,titname,sty,style) [plots colored based on the first input and plot the second input on x axis and the third input on y axis]
#		ColorCVariable: color the second and third depend on this variable
#		x: x axis data
#		y: y axis data"
#		titname: name appears in legend that describes the first input
#		sty: line style ("-o", "-.", etc)
#		style: different log style ("loglog", "logx", "logy", "line")
#
#			example: plotScatter(z,x,y,"-o","loglog") returns a plot
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
# function that plots colored based on the first input and plot the second input on x axis and the third input on y axis the third argument is a name 
# that appears in the legend describing the first input
def plotScatter(ColorCVariable,x,y,titname,sty,style):
	#print "start sorting"
	zippedData = zip(ColorCVariable,x,y)
	#print "zipped"
	zippedData.sort()
	#print "sorted"
	ColorCVariable_out=[]
	x_out=[]
	y_out=[]
	#print zippedData
	ColorCVariable_out,x_out,y_out = zip(*zippedData)
	#print "finished"
	DiffColor = np.unique(ColorCVariable_out)

	colors = []

	for i in range(len(DiffColor)):
    		colors.append((random.uniform(0, 1),random.uniform(0, 1),random.uniform(0, 1)))	
	#print colors

	colorpick=colors[0]

	plt.figure()
	legendP=[]
	j=0;
	
	#print ColorCVariable_out
	#print x_out
	#print y_out
	
	#print len(DiffColor)
	for i in range(len(DiffColor)):
		xpl=[]
		ypl=[]
		#print 'i is: '+ str(i)
		#print 'j is: '+ str(j)
		colorpick=colors[i]
		if (j+1) >= len(ColorCVariable_out)-1:
			break
		if ColorCVariable_out[j+1]==ColorCVariable_out[j]:
			xpl.append(x_out[j])
			ypl.append(y_out[j])
			while ColorCVariable_out[j+1]==ColorCVariable_out[j]:
				#print 'j is: '+ str(j)
				xpl.append(x_out[j+1])
				ypl.append(y_out[j+1])
				if (j+1) < len(ColorCVariable_out)-1:
					j=j+1
				else:
					break
		else:
			xpl.append(x_out[j+1])
			ypl.append(y_out[j+1])
			j=j+1
			while ColorCVariable_out[j+1]==ColorCVariable_out[j]:
				#print 'j is: '+ str(j)
				xpl.append(x_out[j+1])
				ypl.append(y_out[j+1])
				if (j+1) < len(ColorCVariable_out)-1:
					j=j+1
				else:
					break
					
		j=j+1	
		zippedPlot=zip(xpl,ypl)
		#print zippedPlot
		zippedPlot.sort()
		xpl,ypl=zip(*zippedPlot)
		plt.plot(xpl,ypl,sty,color=colorpick,label= titname +': '+str(DiffColor[i]))
		if style=="logy":
			plt.yscale('log', nonposy='mask')
		if style=="logx":
			plt.xscale('log', nonposx='mask')
		if style=="loglog":
			plt.yscale('log', nonposy='mask')
			plt.xscale('log', nonposx='mask')
		plt.hold(True)
		
	if style=="logy" or style=="logx" or style=="loglog":
		print "negative values ignored"
	#print "Finished sorting"
