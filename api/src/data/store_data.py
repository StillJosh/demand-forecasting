# store_data.py
# Description: A brief description of what this file does.
# Author: Joshua Stiller
# Date: 26.12.23


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from src.model.utils import serialize_volume


class StoreData:
    """ Class for storing and manipulating the store dataset."""

    def __init__(self, data_location):
        """
        Parameters
        ----------
        data_location: str,
            The location of the data file.
        """

        self.data_location = data_location
        self.data = pd.read_csv(data_location)
        self.product_ids = self.data.columns
        self.dec_sep = ' '
        self.embeddings_2D = pd.DataFrame(columns=['store_id', 'sku_id', 'embedding_1', 'embedding_2'])


    def get_data(self, product_ids, store_ids):
        """
        Returns the data for given products and stores.

        Parameters
        ----------
        product_ids: int or list of ints
            The product ids.
        store_ids: int or list of ints
            The store ids.

        Returns
        -------
        data: pd.DataFrame
            The data for the given products and stores.
        """

        if isinstance(product_ids, int):
            product_ids = [product_ids]
        if isinstance(store_ids, int):
            store_ids = [store_ids]

        # Select data for the given products and stores
        data = self.data[self.data['sku_id'].isin(product_ids)]
        data = data[data['store_id'].isin(store_ids)]
        return data[['store_id', 'sku_id', 'units_sold']]

    def add_embeddings(self, embeddings, store_ids, product_ids):
        """
        Adds the embeddings to the store data.

        Parameters
        ----------
        embeddings: np.array,
            The embeddings.
        store_ids: list of ints,
            The store ids.
        product_ids: list of ints,
            The product ids.
        """

        # Create dataframe
        embeddings = pd.DataFrame(embeddings, columns=['embedding_1', 'embedding_2'])
        embeddings['store_id'] = store_ids
        embeddings['sku_id'] = product_ids

        # Add to dataframe
        self.embeddings_2D = self.embeddings_2D.append(embeddings)

    def plot_products(self, product_id=0, store_id=0, ax=None):

        """
        Plots the sales of a product as a line plot.

        Parameters
        ----------
        product_id: int,
            The product_id
        store_id: int,
            The store_id

        Returns
        -------

        """

        if ax is None:
            ax = plt.gca()

        data = self.get_data(product_ids=product_id, store_ids=store_id)

        ax.plot(data['units_sold'])

    def plot_forecast(self, product_id, store_id, forecast, start_date=None, show_from=0, ax=None):
        """
        Plots the sales of a product and its forecast as a line plot.

        Parameters
        ----------
        product_id: int,
            The product_id
        store_id: int,
            The store_id
        forecast: array-like,
            The forecasted values.
        start_date: int,
            The date from which the forecast should be plotted.
        show_from: int,
            The date from which the sales should be plotted.

        Returns
        -------

        """

        if ax is None:
            ax = plt.gca()

        # Get the data and initialize the forecast column
        data = self.get_data(product_ids=product_id, store_ids=store_id)
        data['forecast'] = np.nan

        # If no start date is given, start the forecast at the end of the data
        if start_date is None:
            start_date = data.shape[0] - len(forecast)

        # Plot the data and the forecast
        data.iloc[start_date:start_date+len(forecast), -1] = forecast
        data = data.iloc[show_from: start_date + len(forecast)]
        data = data.reset_index()
        data = data.melt(id_vars='index', value_vars=['units_sold', 'forecast'], var_name='type', value_name='volume')

        sns.lineplot(data=data, x='index', y='volume', hue='type', ax=ax)

    def get_serialized_data(self, product_id, store_id, from_point=0, to_point=None):
        """
        Returns the historic sales information of a model as text prompt.

        Parameters
        ----------
        product_id: int,
            The product_id
        store_id: int,
            The store_id
        from_point: int,
            The day from which the data should be considered.
        to_point: int,
            The day until which the data should be considered.

        Returns
        -------
        str: str,
            The serialized data.
        """

        data = self.data[self.data['sku_id'] == product_id]
        data = data[data['store_id'] == store_id]
        data = data['units_sold'].values[from_point:to_point]
        data = [serialize_volume(x, self.dec_sep) for x in data]
        data = ' , '.join(data)
        return data
