from __future__ import print_function, division
from networkx import barabasi_albert_graph
from networkx import degree_pearson_correlation_coefficient
from netutil import R, rewire, load_us
N_STEPS = 1000
N_SIMS = 10

Rs = [0 for _ in range(N_STEPS+1)]
rs = [0 for _ in range(N_STEPS+1)]
for s in range(N_SIMS):
    G = load_us()
    Rs[0] += R(G, n=10)
    rs[0] += degree_pearson_correlation_coefficient(G)
    for t in range(1, N_STEPS+1):
        print(t)
        rewire(G)
        Rs[t] += R(G, n=10)
        rs[t] += degree_pearson_correlation_coefficient(G)
Rs = map(lambda r: r/N_SIMS, Rs)
rs = map(lambda r: r/N_SIMS, rs)
with open('step_us.csv', 'w') as fp:
    fp.write('t,R,r\n')
    fp.write('\n'.join([','.join(r)
                        for r in zip(map(str, range(N_STEPS+1)),
                                     map(str, Rs),
                                     map(str, rs))]))
