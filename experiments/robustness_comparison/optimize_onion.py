import pickle, networkx as nx
from netutil import onion_structure

for i in range(100):
    with open('graph/orig_%02d.pkl'%i, 'rb') as fp:
        G = pickle.load(fp)
    G = onion_structure(G.degree())
    print('graph %i from onion'%i)
    with open('graph/opt_o_%02d.pkl'%i, 'wb') as fp:
        pickle.dump(G, fp)
