#!/usr/bin/python
from __future__ import print_function
import numpy as np
import networkx as nx

from calculate_r import calculateR
from rewire import rewire

N_SIMS = 100
N_STEPS = 1000

N_g = 10
N_t = 6

def main():
        R = np.zeros(N_STEPS+1)
        for _ in range(N_SIMS):
                Gc = nx.barabasi_albert_graph(500, 3) # initialize BA
                R[0] += calculateR(Gc)
                Gbest = Gc.copy()
                Rbest = calculateR(Gbest)
                TList = []
                for t in range(1, N_STEPS+1):
                        GList = []
                        n = 0
                        while n <= N_g:
                                G1 = nx.double_edge_swap(Gc)
                                if not G1 in TList:
                                        GList.append(G1)
                                n += 1

                        Gnew = GList[0]
                        Rnew = calculateR(Gnew)
                        for g in GList[1:]:
                                r = calculateR(g)
                                if r > Rnew:
                                        Gnew, Rnew = g, r

                        if Rnew > Rbest:
                                Gbest, Rbest = Gnew, Rnew
                                TList.append(Gbest.copy())
                                if len(TList) > N_t:
                                        Gc = TList.pop(0)
                        R[t] += Rbest
                        print(Rbest)
                print(_)

        R = R / N_SIMS
        with open('result_tabu.csv', 'w') as fp:
                fp.write('t,Tabu Search\n')
                fp.write('\n'.join(map(lambda c: '%d,%f'%(c[0],c[1]),
                                       zip(range(N_STEPS+1), R))))

if __name__ == '__main__':
        main()
