import numpy as np
import plotly.graph_objects as go, numpy as np
from scipy.integrate import solve_ivp

from ..constants import *


class PFR:
    def __init__(self, w, P, whsv, y0, r):
        self.w = w  # gcat
        self.P = P  # bara
        self.whsv = whsv  # mmol/min/gcat
        self.y0 = y0
        self.Ft0 = whsv * w  # mmol/min
        self.F0 = y0 * self.Ft0  # mmol/min
        self.nmlm = self.F0 * mol_gas_vol["nL/mol"]  # normal mL/min
        self.total_nmlm = self.nmlm.sum()
        self.r = r  # mmol/min/gcat
        self.solve()

    def solve(self):
        def df(w, F):
            Ft = F.sum()
            y = F / Ft
            p = y * self.P
            dFdw = np.array([])
            for i in range(0, len(F)):
                ri = self.r[i](p)  # mass balance
                dFdw = np.append(dFdw, ri)
            return dFdw

        w_span = (0, self.w)
        w_eval = np.linspace(0, self.w, 100)
        solution = solve_ivp(df, w_span, self.F0, t_eval=w_eval)
        self.w = solution.t
        self.F = solution.y
        Ft = np.zeros(len(self.w))
        for Fi in self.F:
            Ft = Ft + Fi
        self.y = []
        for Fi in self.F:
            self.y.append(Fi / Ft)
        self.X = (self.F0[0] - self.F[0]) / self.F0[0] * 100

    def plot_molfrac_vs_w(self, labels):
        fig = go.Figure()
        for i, label in enumerate(labels):
            if label != "inert":
                trace = go.Scatter(x=self.w, y=self.y[i], mode="lines", name=label)
                fig.add_trace(trace)
        fig.update_layout(
            title=dict(text="<b>Mole fractions vs. catalyst mass</b>", x=0.5),
            xaxis_title="<b>Catalyst mass (g)</b>",
            yaxis_title="<b>Mole fraction</b>",
            width=700,
        )
        fig.show()

    def plot_conv_vs_w(self, label, Xeq=None):
        fig = go.Figure()
        trace = go.Scatter(x=self.w, y=self.X, mode="lines", name=label)
        fig.add_trace(trace)
        if Xeq:
            trace = go.Scatter(
                x=self.w,
                y=np.zeros(len(self.w)) + Xeq,
                mode="lines",
                name=f"Equilibrium {label}",
            )
            fig.add_trace(trace)
        fig.update_layout(
            title=dict(text="<b>Conversion vs. catalyst mass</b>", x=0.5),
            xaxis_title="<b>Catalyst mass (g)</b>",
            yaxis_title="<b>Conversion (%)</b>",
            width=800,
        )
        fig.show()
