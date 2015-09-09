__author__ = 'sheridan'

from generator import *
from fuel import *
from load import *
import pandas
import numpy as np
import numpy.random as rand


loads = Load(pd.Series([500]*150), pd.datetime(2015,7,1), timeStep = 'M')

loads = Load(pd.Series([500]*4500), pd.datetime(2015,7,31), timeStep = 'H')
meetLoads = loads.data.copy(deep = True)

beaver = Generator('Beaver', 'CC', 'gas', 8000, 450, 225, 3)
otter = Generator('Otter', 'steam oil', 'oil', 8000, 450, 225, 3)

generators = [beaver, otter]

# notDispatched = pd.Series([list(generators)]*len(loads.data), index = loads.data.index)

genByFuel = {"gas":[], "oil":[], "coal":[]}

for gen in generators:
    genByFuel[gen.fuel] += [gen]
    gen.dispatch = pd.Series([float(0)]*len(loads.data), index = loads.data.index)
    gen.costPerUnit = pd.Series([float(0)]*len(loads.data), index = loads.data.index)


oil = Fuel('oil', pd.Series([4]*150), pd.datetime(2015,7,1),'monthly')
training = pd.read_csv("C:/Users/sheridan/Python Projects/Stack Model/trainingGasPrices.csv")
training.ix[:,2] = pd.Series(float(x[1:]) for x in training.ix[:,2])
gas = Fuel('gas',training.ix[:,2], pd.datetime(2015,7,1), 'monthly')
fuels = [oil, gas]

fuelDict = {"gas":gas, "coal":[], "oil":oil}


# Ignore minCaps for now

for period in loads.data.index:
    for gen in generators:
        gen.costPerUnit[period] = gen.opsAndMaint + float(gen.heatRate)/1000 * fuelDict[gen.fuel].data[period]

for period in loads.data.index:
    notDispatched = list(generators)
    while meetLoads[period] > 0:
        costs = [gen.costPerUnit[period] for gen in notDispatched]
        cheapest = costs.index(min(costs))
        notDispatched[cheapest].dispatch[period] = min(notDispatched[cheapest].peakCapacity, meetLoads[period])
        meetLoads[period] -= notDispatched[cheapest].dispatch[period]
        notDispatched.remove(notDispatched[cheapest])














