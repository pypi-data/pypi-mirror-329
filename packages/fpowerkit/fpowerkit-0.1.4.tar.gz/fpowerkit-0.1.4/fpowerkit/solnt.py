import numpy as np
import math
from .solbase import *

class BusType(IntEnum):
    PQ = 0
    PV = 1
    Slack = 2
    
class NewtonSolver(SolverBase):
    def __init__(self, grid:Grid, eps:float = 1e-6, default_saveto:str = DEFAULT_SAVETO, max_iter:int = 100):
        super().__init__(grid, eps, default_saveto)
        self.Y = grid.YMat()
        self.G, self.B = self.Y.real, self.Y.imag
        self.max_iter = max_iter
    
    def CheckBusType(self, _t:int):
        '''Check the bus type'''
        busType:dict[BusID, BusType] = {}
        slack_cnt = 0
        eq_P:list[int] = []
        eq_Q:list[int] = []
        self.Ps = []
        self.Qs = []
        for i, bus in enumerate(self.grid._busl):
            fixp = fixq = True
            p = -bus.Pd(_t)
            q = -bus.Qd(_t)
            for g in self.grid.GensAtBus(bus.ID):
                if not g.FixedP: fixp = False
                else:
                    assert g.P is not None
                    if isinstance(g.P, TimeFunc): p += g.P(_t)
                    else: p += g.P
                if not g.FixedQ: fixq = False
                else:
                    assert g.Q is not None
                    if isinstance(g.Q, TimeFunc): q += g.Q(_t)
                    else: q += g.Q
            if bus.FixedV:
                if fixp and fixq:
                    raise ValueError(f"Bus {bus.ID}: Invalid bus type PQV")
                elif fixp:
                    busType[bus.ID] = BusType.PV
                    eq_P.append(i)
                elif fixq:
                    raise ValueError(f"Bus {bus.ID}: Invalid bus type VQ")
                else:
                    busType[bus.ID] = BusType.Slack
                    slack_cnt += 1
                    if slack_cnt > 1:
                        raise ValueError('Only one slack bus is allowed')
            else:
                if fixp and fixq:
                    busType[bus.ID] = BusType.PQ
                    bus.V = 1.0
                    eq_P.append(i)
                    eq_Q.append(i)
                elif fixp:
                    raise ValueError(f"Bus {bus.ID}: Invalid bus type: Pθ")
                elif fixq:
                    raise ValueError(f"Bus {bus.ID}: Invalid bus type: Qθ")
                else:
                    raise ValueError(f"Bus {bus.ID}: Invalid bus type: θ")
            self.Ps.append(p)
            self.Qs.append(q)
        self.busType = busType
        if slack_cnt == 0:
            raise ValueError('No slack bus is found')
        return eq_P + eq_Q, len(eq_P)
    
    def dt(self, i:int, j:int) -> float:
        return self.grid._busl[i].theta -self.grid._busl[j].theta
    
    def V(self, i:int) -> float:
        r = self.grid._busl[i].V
        assert isinstance(r, float)
        return r

    def P(self,i:int):
        return self.V(i)*sum(self.V(j)*(
            self.G[i,j]*math.cos(self.dt(i,j))+
            self.B[i,j]*math.sin(self.dt(i,j))
        ) for j in range(self.m))
    
    def Q(self,i:int):
        return self.V(i)*sum(self.V(j)*(
            self.G[i,j]*math.sin(self.dt(i,j))-
            self.B[i,j]*math.cos(self.dt(i,j))
        ) for j in range(self.m))
    
    def H(self, i:int, j:int) -> float:
        if i == j: return self.Q(i)+self.V(i)**2*self.B[i,i]
        return -self.V(i)*self.V(j)*(self.G[i,j]*math.sin(self.dt(i,j)) - self.B[i,j]*math.cos(self.dt(i,j)))
    
    def N(self, i:int, j:int) -> float:
        if i == j: return -self.P(i)-self.V(i)**2*self.G[i,i]
        return -self.V(i)*self.V(j)*(self.G[i,j]*math.cos(self.dt(i,j)) + self.B[i,j]*math.sin(self.dt(i,j)))
    
    def M(self, i:int, j:int) -> float:
        if i == j: return -self.P(i)+self.V(i)**2*self.G[i,i]
        return self.V(i)*self.V(j)*(self.G[i,j]*math.cos(self.dt(i,j)) + self.B[i,j]*math.sin(self.dt(i,j)))
    
    def L(self, i:int, j:int) -> float:
        if i == j: return -self.Q(i)+self.V(i)**2*self.B[i,i]
        return -self.V(i)*self.V(j)*(self.G[i,j]*math.sin(self.dt(i,j)) - self.B[i,j]*math.cos(self.dt(i,j)))
    
    def _solve(self) -> int:
        cnt = 0
        while cnt<self.max_iter:
            y = np.zeros(self.n, dtype=np.float64)
            for i, b in enumerate(self.eqs):
                y[i] = self.Ps[b] - self.P(b) if i < self.n_P else self.Qs[b] - self.Q(b)
            if np.abs(y).max() < self.eps:
                break
            cnt += 1
            J = np.zeros((self.n, self.n), dtype=np.float64)
            for i, b0 in enumerate(self.eqs):
                for j, b1 in enumerate(self.eqs):
                    if i < self.n_P and j <self. n_P: #dp/dθ
                        J[i,j] = self.H(b0, b1)
                    elif i < self.n_P and j >= self.n_P: #V*dp/dV
                        J[i,j] = self.N(b0, b1)
                    elif i >= self.n_P and j < self.n_P: #dp/dV
                        J[i,j] = self.M(b0, b1)
                    elif i >= self.n_P and j >= self.n_P: #V*dq/dV
                        J[i,j] = self.L(b0, b1)
            x = np.linalg.solve(J, -y)
            for i, (x0, b) in enumerate(zip(x, self.eqs)):
                if i < self.n_P: # Δθ
                    self.grid._busl[b].theta += x0
                else: # ΔU/U
                    self.grid._busl[b].V += self.V(b) * x0
        if cnt >= self.max_iter:
            raise ValueError("Bad solution")
        return cnt

    def solve(self, _t:int, /, *, timeout_s:float = 1) -> 'tuple[GridSolveResult, float]':
        '''Get the best result at time _t, return a tuple: (result status, optimal objective value)'''
        self.eqs, self.n_P = self.CheckBusType(_t)
        self.n = len(self.eqs)
        self.m = len(self.grid._bnames)
        try:
            self._solve()
        except ValueError:
            return GridSolveResult.Failed, -1
        for l in self.grid.Lines:
            vi = self.grid.Bus(l.fBus).V_cpx
            vj = self.grid.Bus(l.tBus).V_cpx
            assert vi is not None and vj is not None
            i = (vi-vj)/l.Z
            l.I = abs(i)
            s = vi*i.conjugate()
            l.P = s.real
            l.Q = s.imag
        return GridSolveResult.OK, 0