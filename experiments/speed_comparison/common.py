from __future__ import print_function, division
import sys, pickle
from robust_graph import R

def check_arguments():
    try:
        nettype = sys.argv[1]
    except:
        print('usage: %s [ba|us]'%sys.argv[0])
        sys.exit(1)
    if nettype != 'ba' and nettype != 'us':
        print('pass "ba" or "us"')
        sys.exit(1)

def load_networks():
    nettype = sys.argv[1]
    if nettype == 'ba':
        def load_ba(i):
            with open('graph/ba_%d.pkl'%i, 'rb') as fp:
                G = pickle.load(fp)
            return G
        graphs = list(map(load_ba, range(10)))
    elif nettype == 'us':
        with open('graph/us.pkl', 'rb') as fp:
            G = pickle.load(fp)
        graphs = [G.copy() for _ in range(10)]
    return graphs

def run(swap_method, prefix, init_method=None, steps=500, sims=1, Rn=10):
    check_arguments()
    Rs = [0]*(steps+1)
    networks = load_networks()
    for i, G in enumerate(networks, 1):
        for s in range(1,sims+1):
            try: init_method()
            except: pass
            RG = R(G, n=Rn)
            print('graph#%d sim#%d %d swaps R=%f'%(i, s, 0, RG))
            Rs[0] += RG

            for t in range(1, steps+1):
                G = swap_method(G)
                RG = R(G, n=Rn)
                print('graph#%d sim#%d %d swaps R=%f'%(i, s, t, RG))
                Rs[t] += RG
    Rs = map(lambda r: r/(len(networks)*sims), Rs)
    with open('%s.%s.csv'%(prefix, sys.argv[1]), 'w') as fp:
        fp.write('t,%s.%s\n'%(prefix, sys.argv[1]))
        fp.write('\n'.join([','.join(r)
                            for r in zip(map(str, range(steps+1)),
                                         map(str, Rs))]))
