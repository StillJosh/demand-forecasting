# user_data.py
# Description: A brief description of what this file does.
# Author: Joshua Stiller
# Date: 15.03.24

from src.data.base_data import BaseData
import pandas as pd

class UserData(BaseData):
    
    
    def __init__(self, data, column_mapper):
        if isinstance(data, str):
            data = pd.read_csv(data)
        data.rename(columns=column_mapper, inplace=True)
        super().__init__(data)
