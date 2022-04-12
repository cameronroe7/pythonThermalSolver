# -*- coding: utf-8 -*-
import numpy as np
from designSet import DesignSet
from grid import Grid,MeshSizes

from scipy.sparse import lil_array,csc_array
from scipy import linalg

class Solver():
    def __init__(self,
                 designSet = DesignSet(),
                 grid=Grid(MeshSizes.COARSE)):
        self.designSet = designSet
        self.grid = grid
        #we would prefer these arrays be sparse from the get-go
        self.Ah = np.zeros((self.grid.nodes.item(),self.grid.nodes.item()))
        self.Fh = np.zeros((1,self.grid.nodes.item()))
        self.u = []
        self.T_root = None
    
    def reset(self):
        self.Ah = np.zeros((self.grid.nodes.item(),self.grid.nodes.item()))
        self.Fh = np.zeros((1,self.grid.nodes.item()))
        self.u = []
        self.T_root = None
    
    def makeAInterior(self):
        k_m = self.designSet.k()
        
        for m in range(5):
            for k in range(len(self.grid.theta[m])):
                
                N_global = self.grid.theta[m][k,:]
                X = self.grid.getCoorArray(N_global)
                C = linalg.inv(X)
                area = 0.5 * np.abs(np.det(X))
                
                Ak = np.zeros((3,3))
                
                for alpha in range(3):
                    for beta in range(3):
                        Ak[alpha,beta] = k_m[m] * (C[2,alpha]*C[2,beta] + C[3,alpha]*C[3,beta])*area
                self.Ah[N_global,N_global] += Ak