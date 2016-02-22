import pickle, networkx as nx
from netutil import rewire

swap_num = 10000

for i in range(10):
    with open('graph/graph%02d.pkl'%i, 'rb') as fp:
        G = pickle.load(fp)
    for _ in range(swap_num): rewire(G)
    print('graph %d from new'%i)
    with open('graph/graph_opt_n_%02d.pkl'%i, 'wb') as fp:
        pickle.dump(G, fp)
