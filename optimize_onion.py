import pickle, networkx as nx
from netutil import onion_network

for i in range(10):
    with open('graph/graph%02d.pkl'%i, 'rb') as fp:
        G = pickle.load(fp)
    G = onion_network(G.degree())
    print('graph %i from onion'%i)
    with open('graph/graph_opt_o_%02d.pkl'%i, 'wb') as fp:
        pickle.dump(G, fp)
