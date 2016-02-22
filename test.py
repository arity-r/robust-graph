
import time, random, pickle
import numpy as np, networkx as nx
from netutil import R, s, rewire, onion_network

with open('graph.pkl', 'rb') as fp:
    G0 = pickle.load(fp)
#G0 = nx.barabasi_albert_graph(100, 2)
"""
G1 = onion_network(G0.degree())
print('onion generate')
G2 = G0.copy()
for _ in range(1000): rewire(G2)
print('swapping done')
"""
N = 10
#R0 = sum([R(G0) for _ in range(N)]) / N
R0 = R(G0, n=10)
print(R0)
"""
R1 = sum(p.map(R, [G1]*N)) / N
R2 = sum([R(G2) for _ in range(N)]) / N
print('1: %f --> %f'%(R0, R1))
print('2: %f --> %f'%(R0, R2))
"""
