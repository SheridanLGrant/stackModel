__author__ = 'sheridan'

import pandas as pd


class Generator(object):
    """A single generator"""

    types = ["CC", "CT", "coal", "steam oil", "steam gas"]
    fuels = ["gas", "coal", "oil", "other"]

    def __init__(self, name, type, fuel, heatRate, peakCapacity, minCapacity, opsAndMaint,
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

        # if isinstance(name, str):
        #     self.name = name
        # else:
        #     raise TypeError("Generator name must be a string")
        #
        # if type in Generator.types:
        #     self.type = type
        # else:
        #     raise TypeError("See Generator.types for a list of approved types")
        #
        # if fuel in Generator.fuels:
        #     self.fuel = fuel
        # else:
        #     raise TypeError("See Generator.fuels for a list of approved fuels")
        #
        # if isinstance(heatRate, float) or isinstance(heatRate, int):
        #     self.heatRate = heatRate
        # else:
        #     raise TypeError("Generator heatRate must be a float")
        #
        # if isinstance(peakCapacity, float) or isinstance(peakCapacity, int):
        #     self.peakCapacity = peakCapacity
        # else:
        #     raise TypeError("Generator peakCapacity must be a float")
        #
        # if isinstance(minCapacity, float) or isinstance(minCapacity, int):
        #     self.minCapacity = minCapacity
        # else:
        #     raise TypeError("Generator minCapacity must be a float")
        #
        # if isinstance(opsAndMaint, float) or isinstance(opsAndMaint, int):
        #     self.opsAndMaint = opsAndMaint
        # else:
        #     raise TypeError("Operations and maintenance costs must be a float")

    def __repr__(self):
        return self.name + ", a " + self.type + " generator using " + self.fuel + " fuel"