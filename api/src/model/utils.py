# utils.py
# Description: A brief description of what this file does.
# Author: Joshua Stiller
# Date: 26.12.23


import pandas as pd
import numpy as np

def historic_data_as_text(data, product_ids=None):
    """ Returns the historic sales information of a model as text prompt. """

    if product_ids is None:
        product_ids = data.columns

    str = ''
    for index, row in data.iterrows():
        str += f"day {index.strftime('%Y-%m-%d')}: "
        for product_id in product_ids:
            str += f"Product {product_id} was sold {row[product_id]} times. "
        str += '\n'
    return str



def get_forecast_from_completion(completion):
    """ Returns the forecast from a completion. """

    # Get the forecast from the completion
    forecast = completion.choices[0].message.content

    # Convert the forecast to a dataframe
    forecast = forecast.split('\n')
    forecast = [x.split(':') for x in forecast]
    forecast = pd.DataFrame(forecast, columns=['day', 'sales'])
    forecast['day'] = forecast['day'].str.replace('day ', '')
    forecast['sales'] = forecast['sales'].str.replace('Product 0 was sold ', '')
    forecast['sales'] = forecast['sales'].str.replace(' times.', '')
    forecast['day'] = pd.to_datetime(forecast['day'])
    forecast['sales'] = forecast['sales'].astype(int)

    return forecast


def serialize_volume(volumes, dec_sep=' ', num_sep=','):
    """ Serializes a volume to a string. """

    # Convert the list of volumes to a string where the volumes are separated by num_sep
    volumes = str(volumes).replace(' ', num_sep)

    # Separate each digit by dec_sep
    volumes = dec_sep.join(volumes)
    return volumes


def deserialize_volume(volumes, dec_sep=' ', num_sep=','):
    """ Deserializes a volume from a string. """
    # Remove decimal separators and split the string into separate volumes
    volumes = volumes.replace(dec_sep, '')
    volumes = volumes.split(num_sep)

    # Convert the volumes to floats
    volumes = [float(''.join(volume.split(dec_sep))) for volume in volumes]
    return np.array(volumes)