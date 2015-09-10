__author__ = 'sheridan'

import pandas as pd


class Generator(object):
    """A single generator"""

    types = ["CC", "CT", "coal", "steam oil", "steam gas"]
    fuels = ["gas", "coal", "oil", "other", "none"]

    def __init__(self, name, type, peakCapacity, opsAndMaint, fuel = "none", heatRate = 0, minCapacity = 0,
                 derate = {"summer": 1, "winter": 1}, rampRate = 1000, loc = '', dateBuilt = '',
                 dateDecom = pd.datetime(2100,1,1)):

        self.name = name
        self.type = type

        if fuel in Generator.fuels:
            self.fuel = fuel
        else:
            raise TypeError("See Generator.fuels for a list of approved fuels")

        # self.fuel = fuel
        self.heatRate = heatRate
        self.peakCapacity = peakCapacity
        self.minCapacity = minCapacity
        self.opsAndMaint = opsAndMaint
        self.derate = derate
        self.rampRate = rampRate
        self.loc = loc
        self.dateBuilt = pd.to_datetime(dateBuilt)
        self.dateDecom = dateDecom


    def __repr__(self):
        return self.name + ", a " + self.type + " generator using " + self.fuel + " fuel"