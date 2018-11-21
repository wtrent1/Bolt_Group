import Bolt_Group as bltgrp
import numpy as np
import math as m

BG = bltgrp.BoltGroup()

BG.x = np.array([0,0])
BG.y = np.array([0,3])
BG.theta = 0

BG.centroid()

IC = np.array([5,5])
BG.BoltForces(IC)
##
BG.Pn(2,0)

print(m.sin(1))