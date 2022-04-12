# -*- coding: utf-8 -*-
from scipy.io import loadmat
from enum import Enum
import numpy as np

__grids__ = loadmat("grids")

class Grid():
    def __init__(self, meshSize):
        self.name = meshSize.value
        self.data = __grids__[meshSize.value]
        self.nodes = self.data["nodes"][0][0]
        self.coor = self.data["coor"][0][0]
        
        #reorder the thetas
        self.theta = [self.data["theta"][0][0][0][x] for x in (4,0,1,2,3,5,6)]

    def getCoorArray(self,nodes):
        X = np.ones((3,3))
        nodes = np.reshape(nodes,(3,1))
        X[:,(1,2)] = np.hstack((self.coor[nodes,0], self.coor[nodes,1]))
        return X

    def getGlobalEl(self,k,m):
        sum = 0
        for i in range(m-1):
            sum += len(self.theta[i])
        return k + sum
    
class MeshSizes(Enum):
    COARSE = "coarse"
    MEDIUM = "medium"
    FINE = "fine"