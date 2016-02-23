
import time, random, pickle
import numpy as np, networkx as nx
from netutil import R, s, rewire, onion_network, load_us

with open('graph/graph.pkl', 'rb') as fp:
    G0 = pickle.load(fp)
#G0 = nx.barabasi_albert_graph(100, 2)
#G0 = load_us()
print('load')
G1 = onion_network(G0.degree())
print('onion generate')
G2 = G0.copy()
for _ in range(1000): rewire(G2)
print('swapping done')

N = 100
R0 = R(G0, n=N)
R1 = R(G1, n=N)
R2 = R(G2, n=N)
print('1: %f --> %f'%(R0, R1))
print('2: %f --> %f'%(R0, R2))

