#!/usr/bin/env python

import numpy as np

"""
def get_player_matrices(filename):
    player_matrices = []
    with open(filename, 'r') as infile:
        for line in infile:
            current_player = np.zeros()
            line.split()

            # TODO: split the line and convert to integers
            home_runs =
            triples =
            doubles =
            singles =
            walks =
            outs =

            player_matrix = create_player_matrix(home_runs,
                                                 triples,
                                                 doubles,
                                                 singles,
                                                 walks,
                                                 outs)
            player_matrices.append(player_matrix)
"""

def create_player_matrix(home_runs, triples, doubles, singles, walks, outs):
    # convert to probabilities
    total = home_runs + triples + doubles + singles + walks + outs
    h = homeruns / total
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

def create_run_matrix():
    pass

def get_expected_runs():
    filename = "files/"
    player_matrices = get_player_matrices(filename)
    run_matrix =

get_expected_runs()
