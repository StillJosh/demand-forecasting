# simulation.py
# Description: A brief description of what this file does.
# Author: Joshua Stiller
# Date: 26.12.23


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class SimulatedData:

    def __init__(self, num_products=1, num_days=100):
        self.num_products = num_products
        self.num_days = num_days
        self.data = self._simulate_seasonal(num_products, num_days)
        #self.data = self._simulate_periodic(num_products, num_days)

    def _simulate_periodic(self, num_products=1, num_days=100):
        """ Simulates number of sales from capped sin curve. """

        # Simulate number of sales
        x = np.linspace(0, 12 * np.pi, num_days)
        y = np.maximum(np.sin(x), 0)
        y = np.round(y * 100)
        y = y.astype(int)
        y = np.tile(y, (num_products, 1))

        # Simulate product IDs
        product_ids = np.arange(num_products)
        product_ids = np.tile(product_ids, (num_days, 1))
        product_ids = product_ids.T

        # Simulate dates
        dates = pd.date_range('2020-01-01', periods=num_days, freq='D')
        dates = np.tile(dates, (num_products, 1))

        # Create dataframe
        data = pd.DataFrame({'product_id': product_ids.flatten(), 'date': dates.flatten(), 'sales': y.flatten()})

        data = data.pivot(index='date', columns='product_id', values='sales')


        return data

    def _simulate_seasonal(self, num_products=1, num_days=100, period=10, amplitude=10, phase_shift=0):
        """ Simulates number of sales from a seasonal pattern. """

        # Simulate number of sales
        x = np.linspace(0, 1, num_days)
        scaler = np.arange(num_days) / 100
        y = np.maximum(amplitude * np.sin(2 * np.pi * (np.arange(num_days) + phase_shift) / period), 0) * scaler
        y = np.round(y)
        y = y.astype(int)
        y = np.tile(y, (num_products, 1))

        # Simulate product IDs
        product_ids = np.arange(num_products)
        product_ids = np.tile(product_ids, (num_days, 1))
        product_ids = product_ids.T

        # Simulate dates
        dates = pd.date_range('2020-01-01', periods=num_days, freq='D')
        dates = np.tile(dates, (num_products, 1))

        # Create dataframe
        data = pd.DataFrame({'product_id': product_ids.flatten(), 'date': dates.flatten(), 'sales': y.flatten()})

        data = data.pivot(index='date', columns='product_id', values='sales')

        return data


    def plot_products(self, product_id=0, forecast=None):
        """ Plots the sales of a product. """

        melted_data = sim.data.reset_index().melt(id_vars='date', value_name='sales')
        data = melted_data[melted_data['product_id'] == product_id][:40]
        plt.plot(data['date'], data['sales'])
        if forecast is not None:
            plt.plot(forecast['date'], forecast['sales'])
        plt.show()


sim = SimulatedData(num_products=2, num_days=100)
sim.plot_products()
