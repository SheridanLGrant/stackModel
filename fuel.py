__author__ = 'sheridan'

import pandas as pd
import generator
import numpy as np


class Fuel(object):
    """The time series data for a fuel type"""

    CO2emissions = {"gas": .058, "coal": .108, "oil": .081, "other": 0, "none": 0}
    # Source: http://www.epa.gov/climateleadership/documents/emission-factors.pdf
    # Lignite coal used
    # Fuel Oil No. 2 used


    def __init__(self, type = "none", price = 0, startDate = 0, timeStep = "M", GHGcost = 0, units = "$/MMBtu"):
        if type in generator.Generator.fuels:
            self.type = type
        else:
            raise TypeError("Please enter an appropriate fuel type. See Fuel.fuels.")

        self.CO2factor = Fuel.CO2emissions[type]

        if not type == "none":


            self.data = pd.Series(data = np.array(price))

            # This ensures that the monthly data starts at the beginning of the month
            if timeStep[0] == 'm' or timeStep[0] == 'M':
                self.data.index = pd.date_range(startDate, periods = len(price),
                                                freq = timeStep[0]) + pd.DateOffset(days = 1) + pd.DateOffset(months = -1)
            else:
                self.data.index = pd.date_range(startDate, periods = len(price), freq = timeStep[0])

            # This allows pandas to fill in the data fully. Make sure your fuel data is long enough.
            appendee = pd.Series(self.data[len(self.data)-1],
                                 index = pd.date_range(self.data.index[len(self.data) - 1] + 1, periods = 1,
                                                       freq = self.data.index.freq))
            self.data = self.data.append(appendee)

        else:
            self.data = []


        self.GHGcost = GHGcost
        self.units = units

    def __repr__(self):
        return self.type + " price series of length " + str(len(self.data))