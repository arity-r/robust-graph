#!/usr/bin/python
from __future__ import print_function
import numpy as np
import networkx as nx

from calculate_r import calculateR
from rewire import rewire

N_SIMS = 100
N_STEPS = 1000

def main():
        R = np.zeros(N_STEPS+1)
        for _ in range(N_SIMS):
                G = nx.barabasi_albert_graph(500, 3) # initialize BA
                R[0] += calculateR(G)
                for t in range(1, N_STEPS+1):
                        rewire(G)
                        R[t] += calculateR(G)
        R = R / N_SIMS
        with open('result_new.csv', 'w') as fp:
                fp.write('t,New Algorithm\n')
                fp.write('\n'.join(map(lambda c: '%d,%f'%(c[0],c[1]),
                                       zip(range(N_STEPS+1), R))))

if __name__ == '__main__':
	main()
