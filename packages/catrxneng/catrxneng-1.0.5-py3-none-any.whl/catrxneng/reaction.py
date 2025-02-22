import plotly.graph_objects as go, numpy as np

from catrxneng.constants import *


class Reaction:
    def __init__(self):
        pass

    def dG_rxn(self):
        return self.dH_rxn() - self.T_K * self.dS_rxn()

    def Keq(self):
        return np.exp(-self.dG_rxn() / R["kJ/mol/K"] / self.T_K)

    def plot_K_vs_temp(self):
        fig = go.Figure()
        trace = go.Scatter(x=self.T_C, y=self.Keq(), mode="lines")
        fig.add_trace(trace)
        fig.update_layout(
            title="Equilibrium constant",
            xaxis_title="Temperature (°C)",
            yaxis_title="K"
        ) 
        fig.show()
