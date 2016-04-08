from networkx import double_edge_swap
from robust_graph import R
from common import run

Ng, Nt = 10, 6

swaps = 0
TList, t = [], 0
Gbest, Rbest = None, 0

def init_method():
    global swaps, TList, t, Gbest, Rbest
    swaps = 0
    TList, t = [], 0
    Gbest, Rbest = None, 0

def update_tabu(Gc):
    global swaps, TList, t, Gbest, Rbest
    origswaps = swaps
    trials = 10**2
    while origswaps == swaps and trials:
        trials -= 1
        # store tuple 1st -> graph 2nd -> R
        GList = []
        n = 0
        while n <= Ng:
            G1 = Gc.copy()
            double_edge_swap(G1)
            # graph comparison by comparing edge set
            if len(TList) == 0 or\
               not any(map(lambda T: set(T.edges())==set(G1.edges()),
                           list(zip(*TList))[0])):
                GList.append((G1, R(G1)))
            n += 1

        # findbest
        Gnew, Rnew = max(GList, key=lambda e: e[1])

        if Rnew > Rbest or Rnew > R(Gbest): # only works if you're lazy
        #if Rnew > Rbest:
            print('%f -> %f'%(Rbest, Rnew))
            Gbest, Rbest = Gnew, Rnew

            TList.append((Gbest, swaps+1))
            t += 1
            if t > Nt:
                Gc, swaps = TList.pop(0)
    return Gbest

run(update_tabu, 'tabu', init_method=init_method)

