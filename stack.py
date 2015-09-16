__author__ = 'sheridan'

from generator import *
from fuel import *
from load import *
import numpy as np
import operator

class Stack(object):
    """Builds a stack model with given inputs"""

    seasons = {12: "winter", 1: "winter", 2: "winter", 6: "summer", 7: "summer", 8: "summer"}


    def __init__(self, load, generators, fuels):

        self.load = load
        self.generators = generators
        self.n = len(generators)
        self.fuels = fuels
        self.meetLoad = load.data.copy(deep = True)

        # We added an extra data point in the fuel constructor--now we remove it once we've coerced the
        # time series into the appropriate time step
        for fuel in self.fuels:
            if fuel.type == "none":
                fuel.data = pd.Series([0]*len(load.data), index = load.data.index)
            else:
                fuel.data = fuel.data.resample(load.data.index.freq, fill_method = 'pad')
                fuel.data = fuel.data[:(len(fuel.data)-1)]

        # Similar coercion required for load data in order to get ramping rates done correctly
        appendee = pd.Series(self.load.data[len(self.load.data) - 1],
                             index = pd.date_range(self.load.data.index[len(self.load.data) - 1] + 1, periods = 1,
                                                   freq = self.load.data.index.freq))
        minTS = self.load.data.append(appendee).resample('min').index

        self.genByFuel = {key: [] for key in Generator.fuels}
        for gen in self.generators:
            self.genByFuel[gen.fuel] += [gen]
            gen.dispatch = pd.Series([float(0)]*len(load.data), index = load.data.index)
            gen.fuelUse = pd.Series([float(0)]*len(load.data), index = load.data.index)
            gen.emissions = pd.Series([float(0)]*len(load.data), index = load.data.index)
            gen.costPerUnitNoGHG = pd.Series([float(0)]*len(load.data), index = load.data.index)
            gen.costPerUnitGHG = pd.Series([float(0)]*len(load.data), index = load.data.index)
            gen.costPerUnit = pd.Series([float(0)]*len(load.data), index = load.data.index)
            gen.rampSeries = pd.Series([gen.rampRate]*len(minTS),
                                       index = minTS).resample(self.load.data.index.freq, fill_method = 'pad')
            gen.rampSeries = gen.rampSeries * (len(minTS) - 1)/len(self.load.data)

        self.fuelDict = {key: [] for key in Generator.fuels}
        for fuel in fuels:
            self.fuelDict[fuel.type] += [fuel]

        for period in load.data.index:
            for gen in generators:
                gen.costPerUnitNoGHG[period] = gen.opsAndMaint + float(gen.heatRate)/1000 * self.fuelDict[gen.fuel][0].data[period]
                gen.costPerUnitGHG[period] = float(gen.heatRate)/1000 * Fuel.CO2emissions[gen.fuel] * self.fuelDict[gen.fuel][0].GHGcost
                gen.costPerUnit[period] = gen.costPerUnitNoGHG[period] + gen.costPerUnitGHG[period]


    def __repr__(self):
        return "Stack with load series of length " + str(len(self.load.data)) + " and " + str(len(self.generators)) + " generators."

    def dispatch(self):
        for period in self.load.data.index:
            notDispatched = list(self.generators)
            while self.meetLoad[period] > 0:
                costs = [gen.costPerUnit[period] for gen in notDispatched]
                cheapest = costs.index(min(costs))
                notDispatched[cheapest].dispatch[period] = min(notDispatched[cheapest].peakCapacity*derate(period.month, notDispatched[cheapest]), self.meetLoad[period])
                notDispatched[cheapest].fuelUse[period] = notDispatched[cheapest].dispatch[period]*float(notDispatched[cheapest].heatRate)/1000
                notDispatched[cheapest].emissions[period] = notDispatched[cheapest].fuelUse[period]*Fuel.CO2emissions[notDispatched[cheapest].fuel]
                self.meetLoad[period] -= notDispatched[cheapest].dispatch[period]
                notDispatched.remove(notDispatched[cheapest])

    def costs(self):
        self.dispatch()

        self.totalCost = pd.Series([0]*len(self.load.data), index = self.load.data.index)
        self.totalCostNoGHG = pd.Series([0]*len(self.load.data), index = self.load.data.index)
        self.totalCostGHG = pd.Series([0]*len(self.load.data), index = self.load.data.index)


        for gen in self.generators:
            gen.dispatchCost = gen.dispatch*gen.costPerUnit
            gen.dispatchCostNoGHG = gen.dispatch*gen.costPerUnitNoGHG
            gen.dispatchCostGHG = gen.dispatch*gen.costPerUnitGHG
            self.totalCost += gen.dispatchCost
            self.totalCostGHG += gen.dispatchCostGHG
            self.totalCostNoGHG += gen.dispatchCostNoGHG
            print gen.name + ' costs were ' + str(sum(gen.dispatchCost))

        print 'Total cost was ' + str(sum(self.totalCost))

    def outputExcel(self, path):
        self.costs()

        self.totalGen = sum([gen.dispatch for gen in self.generators])

        n_gen_fields = 4

        output = pd.DataFrame(np.zeros([len(self.load.data), 5 + n_gen_fields*len(self.generators)]))

        columns1 = ['Load', 'Total Generation', 'Unmet Load', 'Total Generation Cost', 'Total Generation GHG Cost']
        columns2 = [map(operator.add, [x]*n_gen_fields,
                        [' Generation', ' Generation Cost', ' Generation GHG Cost',
                         ' Generation Cost per MWh']) for x in [gen.name for gen in self.generators]]

        columns2 = [item for sublist in columns2 for item in sublist]
        output.columns = columns1 + columns2
        output.index = self.load.data.index


        output['Load'] = self.load.data
        output['Total Generation'] = self.totalGen
        output['Unmet Load'] = output['Load'] - output['Total Generation']
        output['Total Generation Cost'] = self.totalCost
        output['Total Generation GHG Cost'] = self.totalCostGHG

        for gen in self.generators:
            output[gen.name + ' Generation'] = gen.dispatch
            output[gen.name + ' Generation Cost'] = gen.dispatchCost
            output[gen.name + ' Generation GHG Cost'] = gen.dispatchCostGHG
            output[gen.name + ' Generation Cost per MWh'] = gen.costPerUnit

        output.to_csv(path)


def derate(month, generator):
    if (month in (12, 1, 2, 6, 7, 8)):
        return generator.derate[Stack.seasons[month]]
    else:
        return 1