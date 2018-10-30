import Bolt_Group as bltgrp
import numpy as np

BG = bltgrp.BoltGroup()

BG.x = np.array([0,3])
BG.y = np.array([0,0])
BG.theta = 0

BG.centroid()

IC = np.array([5,5])
BG.BoltForces(IC)
##
BG.Pn(5,5)
