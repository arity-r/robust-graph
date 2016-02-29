from __future__ import print_function, division
from networkx import barabasi_albert_graph
from networkx import degree_pearson_correlation_coefficient
from robust_graph import R, preferential_rewiring
N_STEPS = 3000
N_SIMS = 10

Rs = [0 for _ in range(N_STEPS+1)]
rs = [0 for _ in range(N_STEPS+1)]
for s in range(N_SIMS):
    G = barabasi_albert_graph(500, 3)
    Rs[0] += R(G, n=10)
    rs[0] += degree_pearson_correlation_coefficient(G)
    for t in range(1, N_STEPS+1):
        print('sim %d step %d'%(s, t))
        preferential_rewiring(G)
        Rs[t] += R(G, n=10)
        rs[t] += degree_pearson_correlation_coefficient(G)
Rs = map(lambda r: r/N_SIMS, Rs)
rs = map(lambda r: r/N_SIMS, rs)
with open('step_ba.csv', 'w') as fp:
    fp.write('t,R,r\n')
    fp.write('\n'.join([','.join(r)
                        for r in zip(map(str, range(N_STEPS+1)),
                                     map(str, Rs),
                                     map(str, rs))]))

