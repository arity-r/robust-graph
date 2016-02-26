import pickle, networkx as nx
from robust_graph import onion_structure
from robust_graph import R

for i in range(100):
    with open('graph/orig_%02d.pkl'%i, 'rb') as fp:
        G = pickle.load(fp)
    R0 = R(G, n=10)
    G = onion_structure(G.degree().values())
    R1 = R(G, n=10)
    print('graph %i from onion R(%f --> %f))'%(i, R0, R1))
    with open('graph/opt_o_%02d.pkl'%i, 'wb') as fp:
        pickle.dump(G, fp)
