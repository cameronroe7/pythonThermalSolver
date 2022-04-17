# -*- coding: utf-8 -*-
import numpy as np
import math

import matplotlib.pyplot as plt
import matplotlib.colors as clr
from matplotlib import cm

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
        #we would prefer these arrays be sparse from their initialization
        self.Ah = csc_array(np.zeros((self.grid.nodes.item(),self.grid.nodes.item())))
        self.Fh = np.zeros((self.grid.nodes.item(),1))
        self.u = []
        self.T_root = None
    
    def reset(self):
        self.Ah = np.zeros((self.grid.nodes.item(),self.grid.nodes.item()))
        self.Fh = np.zeros((1,self.grid.nodes.item()))
        self.u = []
        self.T_root = None
    
    def show(self):
        plt.spy(self.Ah,markersize=0.5)
    
    def makeInterior(self):
        k_m = self.designSet.k
        for m in range(5):
            for N_global in zip(self.grid.theta[m]): #better not to use zip and to iterate over array as lists
                X = self.grid.getCoorArray(N_global)
                C = linalg.inv(X)
                area = 0.5 * np.abs(linalg.det(X))
                
                Ak = np.zeros((3,3))
                
                for alpha in range(3):
                    for beta in range(3):
                        Ak[alpha,beta] = k_m[m] * (C[1,alpha]*C[1,beta] + C[2,alpha]*C[2,beta])*area
                self.Ah[np.ix_(*N_global,*N_global)] += Ak
    
    def makeRobinBoundary(self):
        for N_global in self.grid.theta[5]:
            x = self.grid.coor[N_global,:]
            hk = math.sqrt((x[0,0] - x[1,0])**2 + (x[0,1] - x[1,1])**2) 
            Ak = self.designSet.Bi / 2 * hk * np.array([[2/3,1/3],[1/3,2/3]])
            self.Ah[np.ix_(N_global,N_global)] += Ak
    
    def makeRootBoundary(self):
        for N_global in self.grid.theta[6]:
            x = self.grid.coor[N_global,:]
            hk = math.sqrt((x[0,0] - x[1,0])**2 + (x[0,1] - x[1,1])**2) 
            Fk = hk/2 * np.array([[1],[1]])
            self.Fh[np.ix_([0,0],N_global)] += Fk
            
    def makeAMatrix(self):
        self.reset()
        self.makeInterior()
        self.makeRobinBoundary()
        self.makeRootBoundary()
        
    def solve(self):
        self.u = linalg.solve(self.Ah,self.Fh.T)
        self.T_root = self.Fh @ self.u
    
    def plotsolution(self):
        plt.figure()
        data = self.u/max(self.u)
        cmap = cm.get_cmap('viridis',100)
        for idx in range(5):
            for jdx in self.grid.theta[idx]:
                try:
                    plt.fill(self.grid.coor[jdx,0],self.grid.coor[jdx,1],facecolor=cmap(data[jdx][0]),edgecolor=None,linewidth=None)
                except ValueError:
                    print(cmap(data[jdx]))
        plt.axis('off')
        plt.title('Temperature distribution')
        plt.colorbar(cm.ScalarMappable(clr.Normalize(min(self.u),max(self.u)),cmap))