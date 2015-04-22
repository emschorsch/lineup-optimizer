#!/usr/bin/env python
import numpy as np

from lineuploader import create_player_matrix

"""
 Here's how we get the dimensions (this is true for all files):
   In each inning, there are 24 possible states:
     3 possible numbers of outs (0,1,2) and 8 on-base combinations
     (each base is binary - either occupied or not - for 2^3 = 8 total)
     So 3 out possibilities * 8 on-base possibilities = 24 states per inning.
   There are 9 innings, so there are 9*24 total states, plus one more final
     state for "end of game" for a total of 9*24 + 1 = 217.
   Each player's matrix gives the probability of going to state j given
     that we're in state i now.  That's a 217x217 matrix (could go from any
     state to any state).  Each player has one of these matrices so the
     whole thing is a 9x217x217 matrix.
     """
def readdata(filename):

    playermatrices = np.zeros(( 9 , 9*24+1 , 9*24+1), dtype="float32" )
    
    f = open(filename, 'r')
    lines = f.readlines()

    for i,line in enumerate(lines):
        stats = line.split(',')
        homeruns = int(stats[0])
        triples = int(stats[1])
        doubles = int(stats[2])
        singles = int(stats[3])
        walks = int(stats[4])
        outs = int(stats[5])
        name = stats[6]
        playermatrices[i,:,:] = create_player_matrix(homeruns,triples,
                            doubles,singles,walks,outs)

    f.close()

    return playermatrices
