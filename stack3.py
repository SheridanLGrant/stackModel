__author__ = 'sheridan'

from generator import *
from scipy.optimize import linprog
from pulp import *
from stack import *
from fuel import *
from load import *
import pandas
import numpy as np
import numpy.random as rand

class Stack3(Stack):

    def dispatch(self):
        for period in self.load.data.index:

            x = [LpVariable('x_' + str(i), 0, 1, 'Integer') for i in range(len(self.generators))]
            y = [LpVariable('y_' + str(i), 0, cat = 'Continuous') for i in range(len(self.generators))]
            c = [gen.costPerUnit[period] for gen in self.generators]
            upper = [gen.peakCapacity * derate(period.month, gen) for gen in self.generators]
            lower = [gen.minCapacity for gen in self.generators]

            if period - 1 in self.load.data.index:
                upperRamp = [gen.dispatch[period - 1] + gen.rampSeries[period] for gen in self.generators]
                lowerRamp = [gen.dispatch[period - 1] - gen.rampSeries[period] for gen in self.generators]

            mip = LpProblem('Dispatch', sense = 1)
            mip += lpDot(y, c)
            mip += lpSum(y) == self.load.data[period]
            for i in range(len(self.generators)):
                mip += y[i] <= upper[i] * x[i]
                mip += y[i] >= lower[i] * x[i]
                if period - 1 in self.load.data.index:
                    mip += y[i] <= upperRamp[i] * x[i]
                    mip += y[i] >= lowerRamp[i] * x[i]

            sol = mip.solve()
            # print sol
            # print period

            for i in range(len(self.generators)):
                self.generators[i].dispatch[period] = value(y[i])