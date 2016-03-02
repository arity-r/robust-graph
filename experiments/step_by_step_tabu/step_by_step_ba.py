from __future__ import print_function, division
from networkx import barabasi_albert_graph
from networkx import degree_pearson_correlation_coefficient
from networkx import double_edge_swap
from networkx import is_isomorphic
from robust_graph import R, preferential_rewiring
N_STEPS = 3000
N_SIMS = 1
Ng, Nt = 10, 6

Rs = [0 for _ in range(N_STEPS+1)]

for s in range(N_SIMS):
    Gc = barabasi_albert_graph(500, 3)
    Rc = R(Gc)
    Gbest, Rbest = Gc, Rc
    TList, t = [], 0
    Rs[0] += Rc
    steps = 1
    for _ in range(1, N_STEPS+1):
        print('sim %d step %d R=%f'%(s, steps, Rbest))
        GList = []
        n = 0
        while n <= Ng:
            G1 = Gc.copy()
            double_edge_swap(G1)
            #if not any(map(lambda G: is_isomorphic(G, G1), TList)):
            if not any(map(lambda T: set(T.edges())==set(G1.edges()), TList)):
                GList.append((G1, R(G1)))
            n += 1

        # findbest
        Gnew, Rnew = max(GList, key=lambda e: e[1])

        if Rnew > Rbest:
            Gbest, Rbest = Gnew, Rnew
            TList.append(Gbest)
            t += 1
            if t > Nt:
                Gc = TList.pop(0)

        Rs[steps] += Rbest

Rs = map(lambda r: r/N_SIMS, Rs)
with open('step_ba.csv', 'w') as fp:
    fp.write('t,R\n')
    fp.write('\n'.join([','.join(r)
                        for r in zip(map(str, range(N_STEPS+1)),
                                     map(str, Rs))]))

