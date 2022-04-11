# -*- coding: utf-8 -*-

from scipy.io import loadmat
from enum import Enum

grids = loadmat("grids.mat",struct_as_record=True,squeeze_me=False)

coarse = grids["coarse"]

nodes = coarse["nodes"].item()
coor = coarse["coor"]
theta = coarse["theta"]

class MeshDefinitions(Enum):
    COARSE = "coarse"
    MEDIUM = "medium"
    FINE = "fine"
