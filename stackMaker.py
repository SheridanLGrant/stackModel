__author__ = 'sheridan'

from stack import *
from stack3 import *
import pandas as pd

class StackMaker(object):

    def __init__(self, MIP = False, loadPath = 'S:/Sheridans_Documents/Stack Model/testInputLoad3.csv',
                 genPath= 'S:/Sheridans_Documents/Stack Model/testInputGens4.csv',
                 fuelPaths = ['S:/Sheridans_Documents/Stack Model/testInputOil.csv',
                 'S:/Sheridans_Documents/Stack Model/testInputGas.csv']):

        loadSheet = pd.read_csv(loadPath)
        genSheet = pd.read_csv(genPath).fillna(0)
        fuelSheets = []
        for i in range(len(fuelPaths)):
            fuelSheets += [pd.read_csv(fuelPaths[i])]

        self.load = Load(loadSheet['load'], loadSheet['startDate'][0], loadSheet['timeStep'][0],
                    loadSheet['units'][0])
        self.generators = []
        for i in range(len(genSheet['name'])):
            self.generators += [Generator(genSheet['name'][i], genSheet['type'][i], float(genSheet['peakCapacity'][i]),
                                          float(genSheet['opsAndMaint'][i]), float(genSheet['startupCost'][i]),
                                          genSheet['fuel'][i], float(genSheet['heatRate'][i]),
                                          float(genSheet['minCapacity'][i]),
                                          {"summer": float(genSheet['derate summer'][i]),
                                           "winter": float(genSheet['derate winter'][i])},
                                          genSheet['rampRate'][i], genSheet['loc'][i], genSheet['dateBuilt'][i],
                                          genSheet['dateDecom'][i])]
        self.fuels = []
        for i in range(len(fuelSheets)):
            self.fuels += [Fuel(fuelSheets[i]['type'][0], fuelSheets[i]['price'], fuelSheets[i]['startDate'][0],
                                fuelSheets[i]['timeStep'][0], fuelSheets[i]['GHGcost'][0], fuelSheets[i]['units'][0])]
        # Every stack gets a none-type fuel
        self.fuels += [Fuel()]

        if MIP:
            self.stack = Stack3(self.load, self.generators, self.fuels)
        else:
            self.stack = Stack(self.load, self.generators, self.fuels)

    def runStack(self, path = 'S:/Sheridans_Documents/Stack Model/testOutput.csv'):
        self.stack.outputExcel(path)