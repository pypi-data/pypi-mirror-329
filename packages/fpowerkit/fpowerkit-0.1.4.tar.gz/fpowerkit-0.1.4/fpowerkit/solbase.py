from abc import ABC, abstractmethod
from enum import IntEnum
from .grid import *

DEFAULT_SAVETO = "./fpowerkit_logs/"

class GridSolveResult(IntEnum):
    '''Result of grid solving'''
    Failed = 0
    OK = 1
    OKwithoutVICons = 2 # Deprecated
    SubOKwithoutVICons = 3 # Deprecated
    PartialOK = 4


class SolverBase(ABC):
    def __init__(self, grid:Grid, eps:float = 1e-6, default_saveto:str = DEFAULT_SAVETO, **kwargs):
        self.grid = grid
        self.eps = eps
        self.saveto = default_saveto
    
    def SetErrorSaveTo(self, path:str = DEFAULT_SAVETO):
        self.saveto = path

    @abstractmethod
    def solve(self, grid:Grid, _t:int, /, **kwargs):
        raise NotImplementedError
