
import sys, pickle
from robust_graph import s, R

S = []
N_ATTACK = 100
for i in range(100):
    with open('graph/'+sys.argv[1]+'_%02d.pkl'%i, 'rb') as fp:
        G = pickle.load(fp)
    for _ in range(N_ATTACK):
        S.append(s(G))
S = map(lambda s: s/(100*N_ATTACK), map(sum, zip(*S)))
print('\n'.join(map(str, S)))
