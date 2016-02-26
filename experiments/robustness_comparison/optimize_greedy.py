import pickle, networkx as nx
from robust_graph import R

INIT_TRIAL = 100

for i in range(100):
    with open('graph/orig_%02d.pkl'%i, 'rb') as fp:
        G1 = pickle.load(fp)
    trial = INIT_TRIAL
    R0 = R1 = R(G1, n=10)
    while trial > 0:
        trial -= 1
        G2 = nx.double_edge_swap(G1.copy())
        R2 = R(G2, n=10)
        if R2 > R1:
            trial = INIT_TRIAL
            G1 = G2
            R1 = R2
        print('graph %d: trial %d from greedy'%(i,trial))
    print('graph %d from greedy R(%f --> %f)'%(i, R0, R1))
    with open('graph/opt_g_%02d.pkl'%i, 'wb') as fp:
        pickle.dump(G1, fp)
