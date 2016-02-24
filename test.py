
import time, random, pickle
import numpy as np, networkx as nx
from robust_graph import R, preferential_rewiring, greedy_rewiring, onion_structure

G0 = nx.barabasi_albert_graph(100, 2)

G1 = onion_structure(G0.degree().values())
print('onion generate')

G2 = G0.copy()
for _ in range(200): preferential_rewiring(G2)
print('preferential rewiring done')

G3 = G0.copy()
for _ in range(200): greedy_rewiring(G3)
print('greedy rewiring done')

R0 = R(G0, n=10)
print('1: %f --> %f'%(R0, R(G1, n=10)))
print('2: %f --> %f'%(R0, R(G2, n=10)))
print('3: %f --> %f'%(R0, R(G3, n=10)))
