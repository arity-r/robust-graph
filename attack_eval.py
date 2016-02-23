
import sys, pickle
from netutil import s

S = []
N_ATTACK = 1
for i in range(10):
    with open('graph/'+sys.argv[1]+'%02d.pkl'%i, 'rb') as fp:
        G = pickle.load(fp)
    for _ in range(N_ATTACK):
        S.append(s(G))
S = map(lambda s: s/(10*N_ATTACK), map(sum, zip(*S)))
print('\n'.join(map(str, S)))
