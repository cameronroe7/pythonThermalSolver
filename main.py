# -*- coding: utf-8 -*-
from grid import Grid, MeshSizes
from designSet import DesignSet
from solver import Solver

def main():
    D = DesignSet()
    T = Grid(MeshSizes.MEDIUM) #T for triangulation
    sol = Solver(D,T)
    sol.makeAMatrix()
    sol.solve()
    sol.plotsolution()

if __name__ == "__main__":
    main()