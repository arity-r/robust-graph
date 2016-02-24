import pickle, networkx as nx
from robust_graph import preferential_rewiring

swap_num = 1000

for i in range(100):
    with open('graph/orig_%02d.pkl'%i, 'rb') as fp:
        G = pickle.load(fp)
    for _ in range(swap_num): preferential_rewiring(G)
    print('graph %d from new'%i)
    with open('graph/opt_n_%02d.pkl'%i, 'wb') as fp:
        pickle.dump(G, fp)
