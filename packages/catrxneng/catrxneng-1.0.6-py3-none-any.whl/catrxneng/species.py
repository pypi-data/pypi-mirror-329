import numpy as np

class Species:
    def __init__(self):
        pass
    def check_temps(self):
        if isinstance(self.T_K,np.ndarray):
            if self.T_K.min() < self.min_temp_K or self.T_K.max() > self.max_temp_K: 
                raise ValueError("Invalid temperature.")
        else:
            if self.T_K < self.min_temp_K or self.T_K > self.max_temp_K:
                raise ValueError("Invalid temperature.")

