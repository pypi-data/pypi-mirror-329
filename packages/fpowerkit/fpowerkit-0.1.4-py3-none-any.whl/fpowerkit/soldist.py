from itertools import chain
from gurobipy import GRB, Constr, LinExpr, Model, Var
from gurobipy import quicksum as Qs
from pathlib import Path
from typing import Optional, Union
from dataclasses import dataclass
from collections import deque
import warnings, math
from .solbase import *

VF = Union[Var, float]

@dataclass
class LoadReduceModule:
    '''Load Reduce module'''
    Bus:BusID
    Limit:TimeFunc
    Reduction:FloatVar = None

class _Island:
    def __init__(self, g:Grid, buses:Iterable[BusID], cutlines:set[LineID]):
        self.grid = g
        self.Buses:set[str] = set()
        self.Gens:set[str] = set()
        self.Lines:set[str] = set()
        self.PVWs:set[str] = set()
        self.ESSs:set[str] = set()
        for b in buses:
            self.Buses.add(b)
            self.Gens.update(gen.ID for gen in g._gatb[b])
            self.Lines.update(ln.ID for ln in g._ladjfb[b] if ln.ID not in cutlines)
            self.Lines.update(ln.ID for ln in g._ladjtb[b] if ln.ID not in cutlines)
            self.PVWs.update(p.ID for p in g._patb[b])
            self.ESSs.update(e.ID for e in g._eatb[b])
    
    def __repr__(self):
        return f"Island: {self.Buses}\nGens: {self.Gens}\nLines: {self.Lines}\nPVWs: {self.PVWs}\nESSs: {self.ESSs}"
    
    def __str__(self):
        return self.__repr__()
    
    def BusItems(self):
        for b in self.Buses:
            yield b, self.grid.Bus(b)
    
    def GenItems(self):
        for g in self.Gens:
            yield g, self.grid.Gen(g)
    
    def LineItems(self):
        for l in self.Lines:
            yield l, self.grid.Line(l)
    
    def PVWItems(self):
        for p in self.PVWs:
            yield p, self.grid.PVWind(p)
    
    def ESSItems(self):
        for e in self.ESSs:
            yield e, self.grid.ESS(e)

class IslandResult(IntEnum):
    Undefined = -1
    OK = 0          # The island is solved without overflow
    OverFlow = 1    # The island is solved but overflow
    Failed = 2      # No island is solved

class DistFlowSolver(SolverBase):
    '''DistFlow solver'''
    def __init__(self, grid:Grid, eps:float = 1e-6, default_saveto:str = DEFAULT_SAVETO, /, *, mlrp:float = 0.5):
        '''
        Initialize
            grid: Grid object
            default_saveto: Default path to save the results
            mlrp: Maximum proportion of load reduction
        '''
        super().__init__(grid, eps, default_saveto)
        self._decb:dict[BusID, LoadReduceModule] = {}
        self.C = 1e9
        self._mlrp = mlrp
        self._oflines:set[LineID] = set()
        self._ofbuses:set[BusID] = set()
        self.UpdateGrid()        
    
    @property
    def OverflowLines(self):
        return self._oflines
    
    @property
    def OverflowBuses(self):
        return self._ofbuses
    
    def UpdateGrid(self, cut_overflow_lines:bool = False):
        self._islands = tuple(
            _Island(self.grid, il, self._oflines) for il in self.__detect_islands(cut_overflow_lines)
        )
        self._island_res = [(IslandResult.Undefined, -1.0) for _ in range(len(self._islands))]
    
    def __detect_islands(self, cutofl:bool):
        '''Detect islands'''
        q:deque[BusID] = deque()
        visited:set[BusID] = set()
        islands:list[set[BusID]] = []
        for bus in self.grid.BusNames:
            if bus in visited: continue
            q.append(bus)
            island:set[BusID] = set()
            while len(q) > 0:
                b = q.popleft()
                if b in visited: continue
                visited.add(b)
                island.add(b)
                for line in self.grid._ladjfb[b]:
                    if cutofl and line.ID in self._oflines: continue
                    if line._tBus in visited: continue
                    q.append(line._tBus)
                for line in self.grid._ladjtb[b]:
                    if cutofl and line.ID in self._oflines: continue
                    if line._fBus in visited: continue
                    q.append(line._fBus)
            islands.append(island)
        return islands
    
    @property
    def Islands(self):
        return self._islands
    
    @property
    def IslandResults(self):
        return self._island_res
    
    @property
    def MLRP(self):
        '''Get the maximum load reduction proportion'''
        return self._mlrp
    @MLRP.setter
    def MLRP(self, v:float):
        '''Set the maximum load reduction proportion'''
        if v < 0 or v > 1:
            raise ValueError("Invalid maximum load reduction proportion")
        self._mlrp = v
    
    def AddReduce(self, bus:BusID, limit:TimeFunc, reduction:Optional[FloatVar] = None):
        '''Add a load reduction module'''
        self._decb[bus] = LoadReduceModule(bus, limit, reduction)
    
    def RemoveReduce(self, bus:BusID):
        '''Remove a load reduction module'''
        if bus in self._decb:
            del self._decb[bus]
        
    def GetReduce(self, bus:BusID) -> LoadReduceModule:
        '''Get the load reduction module'''
        return self._decb[bus]
    
    @property
    def DecBuses(self):
        return self._decb
    
    def solve(self, _t: int, /, *, timeout_s:float = 1) -> 'tuple[GridSolveResult, float]':
        '''Get the best result at time _t, return a tuple: (result status, optimal objective value)'''
        allOK = True
        allFail = True
        val = 0
        for i, il in enumerate(self._islands):
            self._island_res[i] = self.__solve(_t, il, timeout_s)
            if self._island_res[i][0] != IslandResult.Failed:
                allFail = False
                val += self._island_res[i][1]
            if self._island_res[i][0] != IslandResult.OK: allOK = False
        if allOK:
            return GridSolveResult.OK, val
        elif allFail:
            print(f"Failed to solve at time {_t}")
            if self.saveto != "":
                p = Path(self.saveto)
                p.mkdir(parents=True, exist_ok=True)
                self.grid.savePQofBus(str(p/f"{_t}_load.csv"), _t)
            return GridSolveResult.Failed, val
        else:
            return GridSolveResult.PartialOK, val
    
    def __solve(self, _t: int, island:_Island, timeout_s:float) -> 'tuple[IslandResult, float]':
        model = Model("model")
        
        ''' ---------Variables----------
        pg0[k]: Generator active power
        qg0[k]: Generator reactive power
        pvwp[k]: PVWind active power
        --> pg[j]: Active power of all generators at the bus
        --> qg[j]: Reactive power of all generators at the bus
        v[j]: Bus voltage ** 2
        l[i,j]: Line current ** 2
        P[i,j]: Line active power
        Q[i,j]: Line reactive power
        '''
        # Create GEN vars
        pg0: dict[str, VF] = {}
        qg0: dict[str, VF] = {}
        for gID, g in island.GenItems():
            if g.FixedP:
                assert g.P is not None
                pg0[gID] = g.P(_t) if isinstance(g.P, TimeFunc) else g.P
            elif g.Pmin is not None and g.Pmax is not None:
                pg0[gID] = model.addVar(name=f"pg_{gID}", vtype='C', lb=g.Pmin(_t), ub=g.Pmax(_t))
            else:
                raise ValueError(f"Generator {gID} provides neither P or (pmin, pmax)")
            if g.FixedQ:
                assert g.Q is not None
                qg0[gID] = g.Q(_t) if isinstance(g.Q, TimeFunc) else g.Q
            elif g.Qmin is not None and g.Qmax is not None:
                qg0[gID] = model.addVar(name=f"qg_{gID}", vtype='C', lb=g.Qmin(_t), ub=g.Qmax(_t))
            else:
                raise ValueError(f"Generator {g.ID} provides neither Q or (qmin, qmax)")
        
        pvwp: dict[str, Var] = {pID: model.addVar(
            name=f"pvw_{pID}", vtype='C', lb=0, ub=p.P(_t)
        ) for pID, p in island.PVWItems()}
        pvwq: dict[str, Var] = {pID: model.addVar(
            name=f"pvw_{pID}", vtype='C', lb=-GRB.INFINITY, ub=GRB.INFINITY
        ) for pID in island.PVWs}

        # Bind GEN vars to Bus
        pg: dict[str, list[VF]] = {b: [] for b in island.Buses}
        qg: dict[str, list[VF]] = {b: [] for b in island.Buses}
        pd: dict[str, float] = {bID: b.Pd(_t) for bID, b in island.BusItems()}
        qd: dict[str, float] = {bID: b.Qd(_t) for bID, b in island.BusItems()}
        for gID, g in island.GenItems():
            pg[g.BusID].append(pg0[gID])
            qg[g.BusID].append(qg0[gID])
        for pID, p in island.PVWItems():
            pg[p.BusID].append(pvwp[pID])
            qg[p.BusID].append(pvwq[pID])
        for eID, e in island.ESSItems():
            p, q = e.GetLoad(_t, island.grid.ChargePrice(_t), island.grid.DischargePrice(_t))
            e.P = p
            if p > 0:
                pg[e.BusID].append(p)
                qg[e.BusID].append(q)
            elif p < 0:
                pd[e.BusID] -= p
                qd[e.BusID] -= q
        
        # Create BUS vars
        v = {bID: model.addVar(name=f"v_{bID}", vtype='C') for bID in island.Buses}
        dvmin:dict[str, Var] = {}
        dvmax:dict[str, Var] = {}
        for bid, b in island.BusItems():
            if b.FixedV:
                assert b.V is not None, f"Bus {bid} has fixed voltage but not set"
                model.addConstr(v[bid] == b.V ** 2)
            else:
                dvmin[bid] = model.addVar(name=f"dvmin_{bid}", vtype='C', lb=0)
                dvmax[bid] = model.addVar(name=f"dvmax_{bid}", vtype='C', lb=0)
                model.addConstr(v[bid] >= b.MinV ** 2 - dvmin[bid])
                model.addConstr(v[bid] <= b.MaxV ** 2 + dvmax[bid])
        
        # Create Line vars
        dlmax:dict[str, Var] = {}
        l = {lID: model.addVar(name=f"l_{lID}", vtype='C', lb=0) for lID in island.Lines}
        for lID, ln in island.LineItems():
            dlmax[lID] = model.addVar(name=f"dlmax_{lID}", vtype='C', lb=0)
            model.addConstr(l[lID] <= (ln.max_I/island.grid.Ib) ** 2 + dlmax[lID])
        
        P = {lID: model.addVar(name=f"P_{lID}", vtype='C', lb=-GRB.INFINITY, ub=GRB.INFINITY) for lID in
             island.Lines}
        Q = {lID: model.addVar(name=f"Q_{lID}", vtype='C', lb=-GRB.INFINITY, ub=GRB.INFINITY) for lID in
             island.Lines}
        
        Pdec:dict[BusID, Var] = {bus: model.addVar(name=f"Pdec_{bus}", vtype='C', 
            lb=0, ub=lim.Limit(_t) * self._mlrp) for bus, lim in self._decb.items()}
        
        # ----------Constraints-----------
        Pcons: dict[str, Constr] = {}
        Qcons: dict[str, Constr] = {}

        for j, bus in island.BusItems():
            flow_in = island.grid.LinesOfTBus(j)
            flow_out = island.grid.LinesOfFBus(j)
            dec = Pdec[j] if j in Pdec else 0
            Pcons[j] = model.addConstr(
                Qs(P[ln.ID] - ln.R * l[ln.ID] for ln in flow_in if ln.ID in island.Lines) + Qs(pg[j]) == Qs(
                P[ln.ID] for ln in flow_out if ln.ID in island.Lines) + pd[j] - dec, f"Pcons_{j}")
            Qcons[j] = model.addConstr(
                Qs(Q[ln.ID] - ln.X * l[ln.ID] for ln in flow_in if ln.ID in island.Lines) + Qs(qg[j]) == Qs(
                Q[ln.ID] for ln in flow_out if ln.ID in island.Lines) + qd[j], f"Qcons_{j}")

        for lid, line in island.LineItems():
            i, j = line.pair
            lid = line.ID
            model.addConstr(
                v[j] == v[i] - 2 * (line.R * P[lid] + line.X * Q[lid]) + (line.R ** 2 + line.X ** 2) * l[lid],
                f"ΔU2_cons_{lid}")
            model.addConstr(P[lid] ** 2 + Q[lid] ** 2 <= l[lid] * v[i], f"SoC_cons_{lid}")
        
        for pID, p in island.PVWItems():
            model.addConstr(pvwp[pID] * math.sqrt(1 - p.PF**2) == pvwq[pID])

        decs = self.C * (Qs(Pdec.values()) + Qs(dvmin.values()) + Qs(dvmax.values()) + Qs(dlmax.values()))
        crpe = Qs(p.CC*(p.P(_t)-pvwp[pID]) for pID, p in island.PVWItems())
        goal = Qs(g.CostA(_t) * pg0[gID] ** 2 + g.CostB(_t) * pg0[gID] + g.CostC(_t) for gID, g in island.GenItems())

        model.setObjective(decs + goal + crpe, GRB.MINIMIZE)
        model.setParam(GRB.Param.OutputFlag, 0)
        model.setParam(GRB.Param.QCPDual, 1)
        model.setParam(GRB.Param.TimeLimit, timeout_s)
        model.setParam(GRB.Param.OptimalityTol, 1e-6)
        model.update()
        model.optimize()

        if model.Status != GRB.Status.OPTIMAL and model.Status != GRB.Status.SUBOPTIMAL:
            for bID, bus in island.BusItems():
                bus._v = bus.ShadowPrice = 0
            for pID, p in island.PVWItems():
                p._pr = p._qr = p._cr = 0
            for lid, line in island.LineItems():
                line.I = line.P = line.Q = 0
            for j, gen in island.GenItems():
                if not gen.FixedP: gen._p = 0
                if not gen.FixedQ: gen._q = 0
            for eID, e in island.ESSItems():
                e.P = 0
            return IslandResult.Failed, -1

        for j, bus in island.BusItems():
            j = bus.ID
            bus._v = v[j].X ** 0.5
            try:
                sp = Pcons[j].Pi
            except:
                sp = None if not self.grid._holdShadowPrice else bus.ShadowPrice
            bus.ShadowPrice = sp

        for lid, line in island.LineItems():
            line.I = l[lid].X ** 0.5
            line.P = P[lid].X
            line.Q = Q[lid].X

        for j, gen in island.GenItems():
            p = pg0[j]
            if isinstance(p, Var): gen._p = p.X
            q = qg0[j]
            if isinstance(q, Var): gen._q = q.X
        
        for pID, p in island.PVWItems():
            p._pr = pvwp[pID].X
            p._qr = pvwq[pID].X
            pgen = p.P(_t)
            p._cr = 1 - p._pr / pgen if pgen > 0 else 0
        
        overflow = False
        self._ofbuses.clear()
        for bID, bv in chain(dvmax.items(), dvmin.items()):
            if bv.X > 1e-6:
                overflow = True
                self._ofbuses.add(bID)
        
        self._oflines.clear()
        for lID, lv in dlmax.items():
            if lv.X > 1e-6:
                overflow = True
                self._oflines.add(lID)
        
        for bus, lim in self._decb.items():
            lim.Reduction = Pdec[bus].X
            if lim.Reduction < 1e-8: lim.Reduction = 0

        return IslandResult.OverFlow if overflow else IslandResult.OK, goal.getValue()