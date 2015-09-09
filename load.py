__author__ = 'sheridan'

import pandas as pd
import numpy as np


class Load(object):
    """The time series data for load"""

    def __init__(self, load, startDate, timeStep = 'Hourly', units = "MWh"):
        self.data = pd.Series(data = np.array(load))
        self.data.index = pd.date_range(startDate, periods = len(load), freq = timeStep[0])
        self.units = units

    def __repr__(self):
        return "Load series of length " + str(len(self.data))