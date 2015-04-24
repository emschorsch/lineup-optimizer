#!/usr/bin/env python
import numpy as np
from math import pow

def create_player_matrix(home_runs, triples, doubles, singles, walks, outs):
    # convert to probabilities
    total = home_runs + triples + doubles + singles + walks + outs
    h = home_runs / total
    t = triples / total
    d = doubles / total
    s = singles / total
    w = walks / total
    o = outs / total

    sub_matrix = np.zeros((8, 8), dtype=float)

    sub_matrix[0] = [h, w+s, d, t, 0, 0, 0, 0]
    sub_matrix[1] = [h, 0, d/2, t, w+s/2, s/2, d/2, 0]
    sub_matrix[2] = [h, s/2, d, t, w, s/2, 0, 0]
    sub_matrix[3] = [h, s, d, t, 0, w, 0, 0]
    sub_matrix[4] = [h, 0, d/2, t, s/6, s/3, d/2, w+s/2]
    sub_matrix[5] = [h, 0, d/2, t, s/2, s/2, d/2, w]
    sub_matrix[6] = [h, s/2, d, t, 0, s/2, 0, w]
    sub_matrix[7] = [h, 0, d/2, t, s/2, s/2, d/2, w]

    transition_matrix = np.zeros((9*24 + 1, 9*24 + 1), dtype=float)
    for i in range(27): # 0 through 26 inclusive
        start = i * 8
        end = i * 8 + 8
        transition_matrix[start:end, start:end] = sub_matrix


    for i in range(9):
        for j in range(2):
            start = (i*24) + (j*8)
            transition_matrix[start:(start+8), (start+8):(start+16)] = o * np.eye(8, dtype=float)

        transition_matrix[(i*24) + 16 : (i*24) + 24, (i+1)*24] = [o]*8#o * np.ones((8,1), dtype=float)

    transition_matrix[9*24, 9*24] = 1

    return transition_matrix

def readdata(filename):

    # player_matrices = np.zeros((9 , 9*24+1 , 9*24+1), dtype="float32" )
    player_matrices = []

    with open(filename, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            stats = line.split(',')
            homeruns = int(stats[0])
            triples = int(stats[1])
            doubles = int(stats[2])
            singles = int(stats[3])
            walks = int(stats[4])
            outs = int(stats[5])
            name = stats[6]
            player_matrix = create_player_matrix(homeruns,
                                                 triples,
                                                 doubles,
                                                 singles,
                                                 walks,
                                                 outs)
            player_matrices.append(player_matrix)

    return player_matrices

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
    smallmat = [[1, 0, 0, 0, 0, 0, 0, 0],
                [2, 1, 1, 1, 0, 0, 0, 0],
                [2, 1, 1, 1, 0, 0, 0, 0],
                [2, 1, 1, 1, 0, 0, 0, 0],
                [3, 2, 2, 2, 1, 1, 1, 0],
                [3, 2, 2, 2, 1, 1, 1, 0],
                [3, 2, 2, 2, 1, 1, 1, 0],
                [4, 3, 3, 3, 2, 2, 2, 1]]

    runmatrix = np.zeros(( 9*24+1 , 9*24+1), dtype='float32' );

    for i in range(9*3):
        runmatrix[ i*8 : i*8+8 , i*8 : i*8+8 ] = smallmat

    return runmatrix

def calculate(order, player_matrices, runmatrix):

    # initial probability is 1 for 0 out, 0 on base, 1st inning
    # all other probabilities are initially zero

    situation = np.zeros( (1, 9*24+1 ), dtype="float32")
    situation[:, 0] = 1

    runs = 0
    batter = 0

    while situation[:, 9*24] < 0.99: # while prob(game not over) >= 0.01
        """
         If you've already read the descriptions of player_matrices and runmatrix
           then you're in good shape to understand what goes on here.
         For each batter, we re-calculate our situation probability vector based
           on the state transition probability matrix of the batter.  If S is
           the situation vector and P is the matrix, the formula is just
           S := S*P
         We also need to keep track of how many runs were scored in those
           transitions.  If R is the matrix of runs for each transition,
           then R.*P is the expected number of runs the player will create for
           each transition.  And, S*(R.*P) is the vector of the expected number
           of runs the player will create if he comes to bat in each state,
           weighted by the probability of each state.  So sum(S*(R.*P)) gives
           the total number of expected runs the batter contributes this time up.

         playermatrix is 9x217x217; to multiply by a single player's matrix,
         so we need to reshape the player's 1x217x217 matrix to be 217x217
         """

        index = order[batter]
        player_matrix = player_matrices[index]
        # player_matrix = np.reshape(player_matrices[index],(9*24+1,9*24+1))

        #import pdb
        #pdb.set_trace()
        temp = np.dot(situation, (runmatrix * player_matrix))
        runs += np.sum(temp);

        situation = np.dot(situation, player_matrix);

        # Get next batter

        batter += 1;
        if batter > 8:
            batter = 0;

    return runs

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

def permute_order(order):
    length = len(order)
    first, second = np.random.choice(range(length), 2, replace=True)
    order[first], order[second] = order[second], order[first]
    return order

if __name__ == '__main__':
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
    player_matrices = readdata('braves.data')
    run_matrix = createrunmatrix()

    order = [0,1,2,3,4,5,6,7,8]

    num_iterations = 10000
    for i in range(num_iterations):
        new_order = permute_order(order.copy())
        current_score = calculate(order, player_matrices, run_matrix)
        new_score = calculate(new_order, player_matrices, run_matrix)
        accept_prob = min(1, pow(3000, 5*(new_score - current_score)))
        # print(accept_prob, new_score, current_score)
        accept = np.random.choice([True, False], p=[accept_prob, 1 - accept_prob])

        if (i % 500 == 0):
            print(order)
            print(current_score, new_score)

        if accept:
            order = new_order

    runs = calculate(order, player_matrices, run_matrix)
    print("This lineup will score an average of %f runs per game.", runs)
