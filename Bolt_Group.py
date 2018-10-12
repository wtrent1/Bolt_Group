import math as m
import numpy as np
import scipy as sp
import scipy.optimize
import matplotlib.pyplot as plt
import sys

class BoltGroup:
    
    def __init__(obj):
##        if len(sys.argv) < 3:
##            Rult = 1
##        assert(isequal(len(x),len(y)),"x and y should be the same size")
        obj.x = 0
        obj.y = 0
        obj.Rult = 1
        obj.theta = 0
        obj.Dmax = 0.34
        obj.rvect = np.array([])
        obj.Rvect = np.array([])
        obj.Rxy = np.array([])
        
    def centroid(obj):
        global xc, xy, size, CG
        xc = np.mean(obj.x)
        yc = np.mean(obj.y)
        size = obj.x.size
        CG = np.array([xc, yc])
        return CG
   
    def Pn(obj,xP,yP):
        # Theta input as degrees clockwise from y-axis
        
        # Convert theta to rads ccw from x-axis
        obj.theta = m.radians(270 - obj.theta)
        
        #some options will go here
        
        global ICo, IC, Pn
        ICo = CG
        IC = sp.optimize.root(Perror(obj,xP,yP), ICo, method='LM')
        #Pn = P(obj,IC)
        #return Pn
   
    def BoltForces(obj,IC):
        # Calculate r values
        global rx, ry
        rx = np.empty(size)
        ry = np.empty(size)
        obj.rvect = np.empty(size)
        
        rx = obj.x - IC[0]
        ry = obj.y - IC[1]
        for i in range(size):
            obj.rvect[i] = m.sqrt(rx[i]**2 + ry[i]**2)
        delta = obj.Dmax * (obj.rvect/max(obj.rvect))
        # Compute strengths of bolts
        global Rx, Ry
        obj.Rvect = np.empty(size)
        angle = np.empty(size)
        Rx = np.empty(size)
        Ry = np.empty(size)
     
        for i in range(size):
            obj.Rvect[i] = obj.Rult * (1 - m.exp(-10*delta[i]))**0.55
            # Component breakdown
            angle[i] = m.atan2(ry[i],rx[i]) + m.pi/2

            Rx[i] = m.cos(angle[i])*obj.Rvect[i]
            Ry[i] = m.sin(angle[i])*obj.Rvect[i]
        obj.Rxy = np.array([Rx,Ry])
        return Rx, Ry
    
    def P(obj,IC):
        BoltForces(IC)
        for i in range(size):
            P = obj.Rvect
        
    def M(obj,IC):
        Rvect = BoltForces(IC)
        M = sum(-Rvect[0,:]*obj.y) + sum(Rvect[1,:]*obj.x)
        
    def plot(obj,CG):
        plt.scatter(obj.x,obj.y)
        plt.show()
        
def Perror(obj,xP,yP,*IC):
    print(IC)
    BoltGroup.BoltForces(obj,IC)
    R = m.sqrt((obj.Rvect[0])**2 + (obj.Rvect[1])**2)
    a = m.sin(obj.theta)
    b = -m.cos(obj.theta)
    c = m.cos(obj.theta)*yP - m.sin(obj.theta)*xP
    e = (a*IC[0] + b*IC[1] + c)/m.sqrt(a**2 + b**2)
    P = sum(obj.rvect*R)/e
    print(P)
    
    return np.array([sum(obj.Rxy[0,:]) + P*m.cos(obj.theta),
                     sum(obj.Rxy[1,:]) + P*m.sin(obj.theta)])
