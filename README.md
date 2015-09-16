# stackModel
Sheridan Grant
Associate, Energy & Environmental Economics

A generation dispatch model with 2 modes:
  1. Simple Mode: Dispatches generators economically, where the only constraint on a generator's output is its peak capacity.        Simply iteratively dispatches the least-cost generator until load is met or all generators are dispatched.
  2. Mixed Integer Programming Mode: Dispatches generators economically, with the following constraints:
      1. Peak and minimum capacity
      2. Ramp Rate
     Mixed integer programming is  used to achieve this non-convex optimization. Currently, this mode only optimizes within a        given time period (and looks to the previous time period for the ramping constraint).

All modes support fuel, O&M, and CO2 cost inputs.

The stackMaker.py wrapper file allows easy construction of a dispatch model from .csv files. Wrapper test files are included in the testing folder in the repository--the input conventions should be easy to glean from these files.

We're interested in improving the MIP mode so that it has moving-window optimization and other functionality to make the dispatch more realistic. Feel free to talk to me or fork the repo if you would like to make updates.
