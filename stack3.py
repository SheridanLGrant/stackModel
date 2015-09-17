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
        count = 0
        for period in self.load.data.index:
            count += 1
            # y = generation
            # x = is generator on or off?
            x = [LpVariable('x_' + str(i), 0, 1, 'Integer') for i in range(len(self.generators))]
            y = [LpVariable('y_' + str(i), 0, cat = 'Continuous') for i in range(len(self.generators))]
            c = [gen.costPerUnit[period] for gen in self.generators]

            # Right now we apply no startup cost at the beginning
            if period - 1 in self.load.data.index:
                s = [(gen.dispatch[period - 1] == 0) * gen.startupCost for gen in self.generators]
            else:
                s = [0] * len(self.generators)

            # Peak/min capacities
            upper = [gen.peakCapacity * derate(period.month, gen) for gen in self.generators]
            lower = [gen.minCapacity for gen in self.generators]

            # Ramping
            if period - 1 in self.load.data.index:
                upperRamp = [gen.dispatch[period - 1] + gen.rampSeries[period] for gen in self.generators]
                lowerRamp = [gen.dispatch[period - 1] - gen.rampSeries[period] for gen in self.generators]

            # Problem and objective function
            mip = LpProblem('Dispatch', sense = 1)
            mip += (lpDot(y, c) + lpDot(x, s))

            # Constraints
            mip += lpSum(y) == self.load.data[period]
            for i in range(len(self.generators)):
                mip += y[i] <= upper[i] * x[i]
                mip += y[i] >= lower[i] * x[i]
                if period - 1 in self.load.data.index:

                    # Generator min up/down time
                    # These will throw at least 1 flag, but not necessarily all flags
                    # as breaking the contraint can lead to not breaking a later constraint that should be broken
                    mip += (x[i] <= ((self.generators[i].dispatch[period - 1] > 0) or \
                                     (sum([(self.generators[i].dispatch[period - j] > 0) \
                                       for j in range(1, min(int(self.generators[i].minDownTime + 1), count))]) == 0)))
                    mip += (x[i] >= ((self.generators[i].dispatch[period - 1] > 0) and \
                                     (sum([(self.generators[i].dispatch[period - j] == 0) \
                                       for j in range(1, min(int(self.generators[i].minUpTime + 1), count))]) > 0)))

                    if self.generators[i].dispatch[period - 1] == 0 and self.generators[i].minCapacity > 0:
                        mip += y[i] <= self.generators[i].minCapacity
                    else:
                        mip += y[i] <= upperRamp[i] * x[i]
                        mip += y[i] >= lowerRamp[i] * x[i]




            sol = mip.solve()
            print count
            print sol
            # print period

            for i in range(len(self.generators)):
                self.generators[i].dispatch[period] = value(y[i])
                self.generators[i].starts[period] = (s[i] * value(x[i])) > 0