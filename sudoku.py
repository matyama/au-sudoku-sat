__author__ = 'matyama'

import getopt
import numpy as np
from sys import argv
from math import sqrt
from subprocess import call
from itertools import product, combinations


def sudoku2sat(n, predefined):

    m = int(sqrt(n))
    M = range(0, m)
    N = range(0, n)

    encode = lambda row, col, val: np.ravel_multi_index((row, col, val), (n, n, n)) + 1
    coord = lambda z, z_offs: m * z_offs + z

    cls = []

    # add predefined values
    for x, y, v in predefined:
        cls.append([encode(x, y, v)])

    # at least one number in each entry
    for x, y in product(N, N):
        cls.append([encode(x, y, v) for v in N])

    # each number at most once in each column/column
    for k, v in product(N, N):
        for i, j in combinations(N, 2):
            cls.append([-encode(k, i, v), -encode(k, j, v)])
            cls.append([-encode(i, k, v), -encode(j, k, v)])

    # each number at most once in each sub-grid
    for v, x_offs, y_offs, x in product(N, M, M, M):
        for y, k in combinations(M, 2):
            cls.append([-encode(coord(x, x_offs), coord(y, y_offs), v), -encode(coord(x, x_offs), coord(k, y_offs), v)])
    for v, x_offs, y_offs, y, l in product(N, M, M, M, M):
        for x, k in combinations(M, 2):
            cls.append([-encode(coord(x, x_offs), coord(y, y_offs), v), -encode(coord(k, x_offs), coord(l, y_offs), v)])

    return cls, len(cls), n ** 3


def display_solution(solution):
    grid = {}
    for x, y, v in solution:
        grid[x, y] = v
    N = range(0, int(sqrt(len(solution))))
    for row in [[grid[x, y]+1 for y in N] for x in N]:
        print(str(row).replace(',', '').strip('[]'))


if __name__ == '__main__':

    predefined = []
    n = 9

    try:
        opts, args = getopt.getopt(argv[1:], 'hi:n:', ['in=', 'n='])
    except getopt.GetoptError:
        print('sudoku.py -i <input_file> -n <size>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('sudoku.py -i <input_file> -n <size>')
            sys.exit()
        elif opt in ('-i', '--in'):
            with open(arg, 'r') as input_file:
                for line in input_file:
                    predefined.append(map(int, line.strip().split()))
        elif opt in ('-n', '--n'):
            n = int(arg)

    # store sudoku SAT as miniSAT DIMACS format
    with open('sudoku.cnf', 'w') as sudoku:
        clauses, num_clauses, num_vars = sudoku2sat(n, predefined)
        print('clauses: %d\tvariables: %d' % (num_clauses, num_vars))
        sudoku.write('p cnf %d %d\n' % (num_vars, num_clauses))
        sudoku.writelines(map(lambda c: str(c).replace(',', '').strip('[]') + ' 0\n', clauses))

    call('./minisat sudoku.cnf sudoku.out', shell=True)

    with open('sudoku.out', 'r') as result_file:
        if result_file.readline().strip() == 'SAT':
            decode = lambda idx: np.unravel_index(idx-1, (n, n, n))
            solution = map(decode, filter(lambda l: l > 0, map(int, result_file.readline().strip().split())))
            display_solution(solution)