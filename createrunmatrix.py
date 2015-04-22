#!/usr/bin/env python
import numpy as np

smallmat = [[1, 0, 0, 0, 0, 0, 0, 0],
            [2, 1, 1, 1, 0, 0, 0, 0],
            [2, 1, 1, 1, 0, 0, 0, 0],
            [2, 1, 1, 1, 0, 0, 0, 0],
            [3, 2, 2, 2, 1, 1, 1, 0],
            [3, 2, 2, 2, 1, 1, 1, 0],
            [3, 2, 2, 2, 1, 1, 1, 0],
            [4, 3, 3, 3, 2, 2, 2, 1]]

"""
This creates the run-value matrix that calculates how many runs will
     score in each transition.  For example, the transition from "0 out,
     runner on 2nd base" to "0 out, 0 on base" must mean that 2 runs have
     scored (because all the baserunners and the batter must either be on
     base somewhere, be out, or have scored)

   It's really a block-diagonal matrix since we're assuming a simplified
     model where no runners advance on outs.  So runs only score when the
     number of outs doesn't change.  
   It's independent of number of outs and independent of the number of
     innings, so the same submatrix (smallmat) appears over and over
     in runmatrix.
   Also, it's independent of the batter so we can store it explicitly
     in a small data file.
"""
def createrunmatrix():

    runmatrix = np.zeros(( 9*24+1 , 9*24+1), dtype='float32' );

    for i in range(9*3):
        runmatrix[ i*8 : i*8+8 , i*8 : i*8+8 ] = smallmat

    return runmatrix
