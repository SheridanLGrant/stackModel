__author__ = 'sheridan'

from generator import *
from scipy.optimize import linprog
from stack import *
from fuel import *
from load import *
import pandas
import numpy as np
import numpy.random as rand

# IS STUPID, NEED MIP
class Stack2(Stack):
    def dispatch(self):
        for period in self.load.data.index:
            # Need to allow generators to turn off
            A = np.concatenate((-np.eye(self.n,self.n), np.eye(self.n, self.n)), 0)
            Aeq = np.array([[1]*self.n])
            Beq = self.load.data[period]
            b = np.array([-gen.minCapacity for gen in self.generators] + [gen.peakCapacity for gen in self.generators])
            c = np.array([gen.costPerUnit[period] for gen in self.generators])

            x = linprog(c, A, b, Aeq, Beq)
            for i in range(len(self.generators)):
                self.generators[i].dispatch[period] = x['x'][i]