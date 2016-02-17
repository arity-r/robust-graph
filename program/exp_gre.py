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
                Gc = nx.barabasi_albert_graph(500, 3) # initialize BA
                Rc = calculateR(Gc)
                R[0] += Rc
                for t in range(1, N_STEPS+1):
                        G1 = nx.double_edge_swap(Gc.copy())
                        R1 = calculateR(G1)
                        if R1 > Rc:
                                Gc, Rc = G1, R1
                        R[t] += Rc
        R = R / N_SIMS
        with open('result_greedy.csv', 'w') as fp:
                fp.write('t,Greedy Algorithm\n')
                fp.write('\n'.join(map(lambda c: '%d,%f'%(c[0],c[1]),
                                       zip(range(N_STEPS+1), R))))

if __name__ == '__main__':
        main()
