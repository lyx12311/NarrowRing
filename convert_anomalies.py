#!/usr/bin/python 

# Thomas Rimlinger, 8 August 2018
# Conversion routines between mean, eccentric, and true anomalies.
import math
import sys

r2d = 180./math.pi
twopi = 2.*math.pi

def outofbounds_e(e):
    if e < 0. or e >= 1.0:
        sys.exit('Must have 0 <= e < 1')

def center(theta):
    if theta > twopi:
        while theta > twopi:
            theta = theta - twopi
    if theta < 0.:
        while theta < 0.:
            theta = theta + twopi
    return theta

# all converstion routines assume angle given in radians
# true anomaly to mean anomaly
def v2M(v, e):
    outofbounds_e(e)
    if v == 0 or v == math.pi:
        return v
    E = v2E(v, e) 
    return center(E2M(E, e))

# true anomaly to eccentric anomaly
def v2E(v, e):
    outofbounds_e(e)
    if v == 0 or v == math.pi:
        return v
    factor = math.sqrt((1.-e)/(1.+e))*math.tan(0.5*v)
    return center(2.*math.atan(factor))

# mean anomaly to true anomaly
def M2v(M, e):
    outofbounds_e(e)
    if M == 0 or M == math.pi:
        return M
    E = M2E(M, e)
    return center(E2v(E, e))

# mean anomaly to eccentric anomaly
def M2E(M, e):
    outofbounds_e(e)
    if M == 0 or M == math.pi:
        return M
    tol = 1.0e-14
    k = 0.85
    x = M - int(M/twopi)*twopi
    if x == 0:
        return 0
    elif x > 0:
        x = x + k*e
    elif x < 0:
        x = x - k*e
    new_x = 0
    num_it = 0
    while abs(x - new_x) > tol:
        if num_it != 0:
            x = new_x
        esinx = e*math.sin(x)
        ecosx = e*math.cos(x)
        f = x - esinx - M
        dfdx = 1 - ecosx
        df2dx2 = esinx
        df3dx3 = ecosx
        dn1 = -f/dfdx
        dn2 = -f/(dfdx + 0.5*dn1*df2dx2)
        dn3 = -f/(dfdx + 0.5*dn2*df2dx2 + dn2*dn2*df3dx3/6.0)
        new_x = x + dn3
        num_it += 1
    return center(new_x)

# eccentric anomaly to true anomaly
def E2v(E, e):
    outofbounds_e(e)
    if E == 0 or E == math.pi:
        return E
    factor = math.sqrt((1.+e)/(1.-e))*math.tan(0.5*E)
    return center(2.*math.atan(factor))

# eccentric anomaly to mean anomaly
def E2M(E, e):
    outofbounds_e(e)
    if E == 0 or E == math.pi:
        return E
    return center(E - e*math.sin(E)) # Kepler's equation

