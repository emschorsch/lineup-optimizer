#!/usr/bin/env python
import numpy as np

from createrunmatrix import createrunmatrix
from readdata import readdata
from calculate import calculate

def battingorder(filename):
    playermatrices = readdata('braves.data')
    runmatrix = createrunmatrix()

    order = inputorder()
    print(order)

    runs = calculate(order, playermatrices, runmatrix)
    print("This lineup will score an average of %f runs per game.", runs)

def inputorder():
    temp = input("Please input the batting lineup: ")
    order = [0]*9
    if len(temp) < 2:
        print("Using default order")
        return order
    elif len(temp) != 9:
        print("Lineup should be nine numbers eg 012345678. Using default lineup instead")
        return order
    else:
        for i, char in enumerate(temp):
            try:
                order[i] = int(char)
            except:
                print("Input should be all numbers eg 012345678. Using default lineup instead")
                return order

    return order



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
#for i in range(9):
 #   battingorder("test")
battingorder("test")
