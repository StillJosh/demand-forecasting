# scaler.py
# Description: A brief description of what this file does.
# Author: Joshua Stiller
# Date: 30.12.23


import numpy as np


class QuantileScaler:

    def __init__(self, upper_quant = 0.95):
        self.upper_quant = upper_quant
        self.upper_quantile = None

    def fit(self, data):
        self.upper_quantile = np.maximum(np.quantile(data, self.upper_quant), 0.1)

    def transform(self, data):
        return data / self.upper_quantile

    def inverse_transform(self, data):
        return data * self.upper_quantile

    def fit_transform(self, data):
        self.fit(data)
        return self.transform(data)