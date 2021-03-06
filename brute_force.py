from battingorder import *
from itertools import permutations

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Brute force.')
    parser.add_argument("filename", nargs='?', default='braves.data', help="file with necessary statistics")
    args = parser.parse_args()

    player_matrices = readdata(args.filename)
    run_matrix = createrunmatrix()

    start_order = list(range(9))

    samples = []
    max_score = 0
    for order in permutations(start_order):
        score = calculate(order, player_matrices, run_matrix)
        if score > max_score:
            max_score = score
            print("score: ", score, order)
        samples.append((score, order))

    samples.sort(reverse=True)
    best = samples[0]

    print("Final ordering: {}".format(best[1]))
    print("This lineup will score an average of {} runs per game.".format(best[0]))
