import pickle, networkx as nx
from robust_graph import preferential_rewiring
from robust_graph import R
swap_num = 100

for i in range(100):
    with open('graph/orig_%02d.pkl'%i, 'rb') as fp:
        G = pickle.load(fp)
    R0 = R(G, n=10)
    for _ in range(swap_num): preferential_rewiring(G)
    R1 = R(G, n=10)
    print('graph %d from preferential rewiring R(%f --> %f)'%(i, R0, R1))
    with open('graph/opt_n_%02d.pkl'%i, 'wb') as fp:
        pickle.dump(G, fp)
