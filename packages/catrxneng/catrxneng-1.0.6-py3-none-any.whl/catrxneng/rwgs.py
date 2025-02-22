from catrxneng import CO, CO2, H2, H2O, Reaction


class RWGS(Reaction):
    def __init__(self,temp_C):
        self.T_C = temp_C
        self.T_K = self.T_C + 273
        self.co = CO(temp_C)
        self.co2 = CO2(temp_C)
        self.h2 = H2(temp_C)
        self.h2o = H2O(temp_C)

    def dH_rxn(self):
        return self.co.Hf() + self.h2o.Hf() - self.co2.Hf() - self.h2.Hf()

    def dS_rxn(self):
        return self.co.Sf() + self.h2o.Sf() - self.co2.Sf() - self.h2.Sf()