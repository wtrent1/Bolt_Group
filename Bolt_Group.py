import math as m
import numpy as np
import scipy as sp
import scipy.optimize
import matplotlib.pyplot as plt
import sys

class BoltGroup:
    def __init__(obj):
        # if len(sys.argv) < 3:
        #     Rult = 1
        # assert(isequal(len(x),len(y)),"x and y should be the same size")
        obj.x = 0
        obj.y = 0
        obj.Rult = 1
        obj.theta = 0
        obj.Dmax = 0.34
        obj.rvect = []
        obj.Rvect = []
        
    def centroid(obj):
        global xc, size, CG
        xc = np.mean(obj.x)
        yc = np.mean(obj.y)
        size = obj.x.size
        CG = np.array([xc, yc])
        return CG
   
    def Pn(obj,xP,yP):
        # Theta input as degrees clockwise from y-axis
        
        # Convert theta to rads ccw from x-axis
        obj.theta = m.radians(90 - obj.theta)
        
        # some options will go here
        
        global ICo, IC, Pn
        ICo = obj.centroid()
        IC = sp.optimize.root(Perror, ICo, args=(obj,xP,yP,), method='lm')
        Pn = obj.P_IC(IC.x)
        print(Pn)
        return Pn
   
    def BoltForces(obj,IC):
        # Calculate r values
        global rx, ry
        rx = np.empty(size)
        ry = np.empty(size)
        obj.rvect = np.empty(size)
        
        ICx = IC[0]
        ICy = IC[1]
        
        # Calculate r values
        rx = obj.x - ICx
        ry = obj.y - ICy
        for i in range(size):
            obj.rvect[i] = m.sqrt(rx[i]**2 + ry[i]**2)
        
        # Compute delta
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
        return Rx, Ry
    
    def P_IC(obj,IC):
        obj.BoltForces(IC)
        P = m.sqrt((sum(Rx))**2 + (sum(Ry))**2)
        return P    
        
    def M(obj,IC):
        obj.BoltForces(IC)
        M = sum(-Rx*obj.y) + sum(Ry*obj.x)
        return M
        
    def plot(obj,CG):
        plt.scatter(obj.x,obj.y)
        plt.show()
        
def Perror(IC,obj,xP,yP):
    
    ICx = IC[0]
    ICy = IC[1]
    
    BoltGroup.BoltForces(obj,IC)
    
    global R, r
    R = np.empty(size)
    r = np.empty(size)
        
    for i in range(size):
        R[i] = m.sqrt(Rx[i]**2 + Ry[i]**2)
    
    # Calculate r values
    rx = obj.x-ICx
    ry = obj.y-ICy
    
    for i in range(size):
        r[i] = m.sqrt(rx[i]**2 + ry[i]**2)
    
    a = m.sin(obj.theta)
    b = -m.cos(obj.theta)
    c = m.cos(obj.theta)*yP - m.sin(obj.theta)*xP
    e = (a*ICx + b*ICy + c)/m.sqrt((a)**2 + (b)**2)
    P = sum(obj.rvect*R)/e
    
    errorx = sum(Rx) + P*m.cos(obj.theta)
    errory = sum(Ry) + P*m.sin(obj.theta)
    error = np.array([errorx, errory])
    # print(error)
    # print(IC)
    
    return error
