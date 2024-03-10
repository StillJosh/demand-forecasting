# base_data.py
# Description: A brief description of what this file does.
# Author: Joshua Stiller
# Date: 06.01.24

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from src.model.utils import serialize_volume


class BaseData:
    
    """ Class for storing and manipulating the customer dataset."""

    def __init__(self, data):
        """
        Parameters
        ----------
        data: pd.DataFrame,
            The location of the data file.
        """

        self._data = data
        self.skus = data['sku'].unique()
        self.customer_ids = data['customer_id'].unique()
        self.dec_sep = ' '
        self.embeddings_2D = pd.DataFrame(columns=['customer_id', 'sku', 'embedding_1', 'embedding_2'])
        self.embeddings = pd.DataFrame(columns=['customer_id', 'sku', 'embedding'])


    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data
        self.skus = data['sku'].unique()
        self.customer_ids = data['customer_id'].unique()

    def get_data(self, product_ids=None, customer_ids=None):
        """
        Returns the data for given products and customers.

        Parameters
        ----------
        product_ids: int or list of ints
            The product ids.
        customer_ids: int or list of ints
            The customer ids.

        Returns
        -------
        data: pd.DataFrame
            The data for the given products and customers.
        """

        if isinstance(product_ids, int):
            product_ids = [product_ids]
        if isinstance(customer_ids, int):
            customer_ids = [customer_ids]

        if self.data.sku.dtype == 'O' and product_ids is not None:
            product_ids = [str(x) for x in product_ids]
        if self.data.customer_id.dtype == 'O' and customer_ids is not None:
            customer_ids = [str(x) for x in customer_ids]

        # Select data for the given products and customers
        data = self.data

        groupby_columns = ['month']
        return_columns = ['month', 'units_sold']

        if product_ids is not None:
            data = data[self.data['sku'].isin(product_ids)]
            groupby_columns.append('sku')
            return_columns.append('sku')
        if customer_ids is not None:
            data = data[data['customer_id'].isin(customer_ids)]
            groupby_columns.append('customer_id')
            return_columns.append('customer_id')

        return data[return_columns].groupby(groupby_columns).sum().reset_index()

    def add_embeddings(self, embeddings, customer_ids, product_ids):
        """
        Adds the embeddings to the customer data.

        Parameters
        ----------
        embeddings: np.array,
            The embeddings.
        customer_ids: list of ints,
            The customer ids.
        product_ids: list of ints,
            The product ids.
        """

        # Create dataframe
        embeddings = pd.DataFrame(embeddings, columns=['embedding_1', 'embedding_2'])
        embeddings['customer_id'] = customer_ids
        embeddings['sku'] = product_ids

        # Add to dataframe
        self.embeddings_2D = self.embeddings_2D.append(embeddings)

    def plot_products(self, product_id=0, customer_id=0, ax=None):

        """
        Plots the sales of a product as a line plot.

        Parameters
        ----------
        product_id: int,
            The product_id
        customer_id: int,
            The customer_id

        Returns
        -------

        """

        if ax is None:
            ax = plt.gca()

        data = self.get_data(product_ids=product_id, customer_ids=customer_id)

        ax.plot(data['month'], data['units_sold'])

    def plot_forecast(self, product_id, customer_id, forecast, start_date=None, show_from=0, ax=None):
        """

        Plots the sales of a product and its forecast as a line plot.

        Parameters
        ----------
        product_id: int,
            The product_id
        customer_id: int,
            The customer_id
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
        data = self.get_data(product_ids=product_id, customer_ids=customer_id)
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

    def get_serialized_data(self, product_id, customer_id, from_point=0, to_point=None):
        """
        Returns the historic sales information of a model as text prompt.

        Parameters
        ----------
        product_id: int,
            The product_id
        customer_id: int,
            The customer_id
        from_point: int,
            The day from which the data should be considered.
        to_point: int,
            The day until which the data should be considered.

        Returns
        -------
        str: str,
            The serialized data.
        """

        data = self.data[self.data['sku'] == product_id]
        data = data[data['customer_id'] == customer_id]
        data = data['units_sold'].values[from_point:to_point]
        data = [serialize_volume(x, self.dec_sep) for x in data]
        data = ' , '.join(data)
        return data
