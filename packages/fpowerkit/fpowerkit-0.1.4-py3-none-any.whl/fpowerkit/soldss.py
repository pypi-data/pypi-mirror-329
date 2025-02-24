from .solbase import *

class OpenDSSSolver(SolverBase):
    
    def __init__(self, grid:Grid, eps:float = 1e-6, default_saveto:str = DEFAULT_SAVETO, max_iter:int = 100, init_t:int = 0, source_bus:str=""):
        super().__init__(grid, eps, default_saveto)
        from py_dss_interface import DSS
        self._g = grid
        t = init_t
        d = DSS()
        d.text("clear")
        cir = f"new circuit.my_circuit basekv={grid.Ub} pu=1.0 phases=3"
        if source_bus != "":
            cir += f" bus1={source_bus}"
        d.text(cir)
        for bus in grid.Buses:
            bid = bus.ID
            p = bus.Pd(t) * grid.Sb_kVA
            q = bus.Qd(t) * grid.Sb_kVA
            print(f"bus {bid} Pd={p} Qd={q}")
            d.text(f"New Load.{bid} bus1={bid}.1.2.3 phases=3 kW={p} kvar={q} vmin={bus.MinV} vmax={bus.MaxV}")
        for line in self.grid.Lines:
            fid = line.fBus
            tid = line.tBus
            d.text(f"New Line.{line.ID} bus1={fid}.1.2.3 bus2={tid}.1.2.3 length={line.L} units=km R1={line.R*grid.Zb} units=ohm X1={line.X*grid.Zb} units=ohm")
        for gen in self.grid.Gens:
            if gen.P is None:
                p = None
            else:
                p = gen.P(t) if isinstance(gen.P, TimeFunc) else gen.P
            if gen.Q is None:
                q = None
            else:
                q = gen.Q(t) if isinstance(gen.Q, TimeFunc) else gen.Q
            bid = gen.BusID
            s = f"New Generator.{gen.ID} bus1={bid} phases=1 kv={grid.Ub} "
            if p is not None:
                s += f"kw={p*grid.Sb_kVA} "
            if q is not None:
                s += f"kvar={q*grid.Sb_kVA} "
            d.text(s)
        d.text("set mode=snapshot")
        self.dss = d

    def solve(self, _t:int, /, *, timeout_s:float = 1) -> 'tuple[GridSolveResult, float]':
        self.dss.text("solve")
        return GridSolveResult.OK, 0.0