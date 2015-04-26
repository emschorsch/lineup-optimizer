from battingorder import *

def permute_order(order):
    length = len(order)
    first, second = np.random.choice(range(length), 2, replace=True)
    order[first], order[second] = order[second], order[first]
    return order

def MCMC(player_matrices, run_matrix, order, num_iterations, print_every):
    for j in range(args.num_iterations):
        new_order = permute_order(order.copy())
        current_score = calculate(order, player_matrices, run_matrix)
        new_score = calculate(new_order, player_matrices, run_matrix)
        accept_prob = min(1, pow(3000, 5*(new_score - current_score)))
        accept = np.random.choice([True, False], p=[accept_prob, 1 - accept_prob])

        if accept:
            order = new_order

        if (j % print_every == 0):
            print(j, order)

    runs = calculate(order, player_matrices, run_matrix)

    return (runs, order)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find the best batting lineup.')
    parser.add_argument("num_iterations", type=int, help="number of iterations for MCMC")
    parser.add_argument("num_samples", type=int, help="number of samples taken")
    parser.add_argument("print_every", type=int, help="print every nth lineup")
    parser.add_argument("filename", nargs='?', default='braves.data', help="file with necessary statistics")
    args = parser.parse_args()

    player_matrices = readdata(args.filename)
    run_matrix = createrunmatrix()

    order = [0,1,2,3,4,5,6,7,8] # default ordering

    samples = []
    for i in range(args.num_samples):
        print("Sample", i+1, ":")
        result = MCMC(player_matrices,
                      run_matrix,
                      order,
                      args.num_iterations,
                      args.print_every)
        samples.append(result)



    samples.sort(reverse=True)
    best = samples[0]

    print("Final ordering: {}".format(best[1]))
    print("This lineup will score an average of {} runs per game.".format(best[0]))
