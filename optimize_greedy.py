import pickle, networkx as nx
from netutil import R

for i in range(1):
    with open('graph/graph%02d.pkl'%i, 'rb') as fp:
        G = pickle.load(fp)
    trial = 1
    Rg = R(G, n=10)
    while trial > 0:
        trial -= 1
        G0 = nx.double_edge_swap(G.copy())
        Rg0 = R(G0, n=10)
        if Rg0 > Rg:
            trial = 0
            G = G0
            Rg = Rg0
    with open('graph/graph_opt_g_%02d.pkl'%i, 'wb') as fp:
        pickle.dump(G, fp)
