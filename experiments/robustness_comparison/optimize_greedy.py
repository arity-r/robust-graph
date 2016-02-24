import pickle, networkx as nx
from robust_graph import R

for i in range(100):
    with open('graph/orig_%02d.pkl'%i, 'rb') as fp:
        G = pickle.load(fp)
    trial = 10
    Rg = R(G, n=10)
    while trial > 0:
        trial -= 1
        G0 = nx.double_edge_swap(G.copy())
        Rg0 = R(G0, n=10)
        if Rg0 > Rg:
            trial = 100
            G = G0
            Rg = Rg0
        print('graph %d: trial %d from greedy'%(i,trial))
    with open('graph/opt_g_%02d.pkl'%i, 'wb') as fp:
        pickle.dump(G, fp)
