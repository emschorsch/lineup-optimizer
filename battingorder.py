#!/usr/bin/env python
import numpy as np

from createrunmatrix import createrunmatrix
from readdata import readdata
from calculate import calculate

def battingorder(filename, order):
    playermatrices = readdata('braves.data')
    runmatrix = createrunmatrix()

    #order = [5]*9

    runs = calculate(order, playermatrices, runmatrix)
    print("This lineup will score an average of %f runs per game.", runs)

"""
Try 9 copies of each batter
Results are:
This lineup will score an average of %f runs per game. 9.60140189459
This lineup will score an average of %f runs per game. 4.76948439237
This lineup will score an average of %f runs per game. 10.8520288514
This lineup will score an average of %f runs per game. 4.60449504573
This lineup will score an average of %f runs per game. 3.73024487193
This lineup will score an average of %f runs per game. 7.40812596236
This lineup will score an average of %f runs per game. 5.71254887106
This lineup will score an average of %f runs per game. 6.26625113282
This lineup will score an average of %f runs per game. 0.225582535146

Seems remotely correct that 3rd batter has the highest expected runs
"""
for i in range(9):
    battingorder("test", [i]*9)

