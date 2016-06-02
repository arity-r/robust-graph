from __future__ import division, absolute_import
import random, networkx as nx
from robust_graph import R
from robust_graph import LOG_LEVEL_QUIET
from robust_graph import Optimizer

class WuHolme(Optimizer):
    """
    Algorithm based on configuration model
    :cite:`Holme2002`

    :param networkx.Graph graph: Graph to be optimized
    :param int log_level: Log level defined in
        :mod:`robust_graph.optimize.log_level`
    :param bool force_update: Ignored
    :param int max_trials: The maximum number of trials for swapping
    :param int a: Parameter in :cite:`Holme2002`
    """
    def __init__(self, graph,
                 log_level=LOG_LEVEL_QUIET,
                 force_update=True,
                 max_trials=100,
                 a=3):
        super(WuHolme, self).__init__(
            graph, log_level, force_update,
            max_trials=max_trials, a=a)

    def optimize(self, steps=1):
        """
        :param int steps: Ignored
        """
        if steps < 0:
            self.log_e('steps cannot be negative value')
        if steps > 1:
            self.log_w('multiple step is ignored in this algorithm')

        G = self._graph.copy()

        # extracting configurations
        max_trials = self._config['max_trials']
        a = self._config['a']

        Rorig = R(G)

        deg = G.degree()
        G = nx.Graph()
        G.add_nodes_from(deg.keys())
        stubs = sum(map(lambda i: [i[0]]*i[1], deg.items()), [])
        mindeg = min(deg.values())
        layer = sum(map(lambda k: [k-mindeg]*k, deg.values()), [])
        stubs = list(zip(stubs, layer))

        trials = 0
        while trials < max_trials and len(stubs) > 0\
              or len(G.edges()) == 0:
            trials += 1
            # 0 --> vertex, 1 --> layer index
            (i, si), (j, sj) = random.sample(stubs, 2)
            if _is_valid_to_add(G, i, j) and \
               random.uniform(0, 1) < 1 / (1+a*abs(si-sj)):
                # link i and j
                self.log_v(
                    'link stabs {0:s} and {1:s} (s = {2:d} and {3:d})'
                    .format(str(i), str(j), si, sj)
                )
                G.add_edge(i, j)
                stubs.remove((i, si))
                stubs.remove((j, sj))

        # no further stabs
        if len(stubs) == 0:
            Rnew = R(G)
            self.log_v(
                'optimize success R = {0:3f} -> {1:3f} after {2:d} trials'
                .format(Rorig, Rnew, trials)
            )
            return True, G

        self.log_v(
            'finished 1st stage after {0:d} trials'
            .format(trials))
        # 2nd stage: detach and re-link

        trials = 0
        while trials < max_trials and len(stubs) > 0:
            trials += 1
            (i, si), (j, sj) = random.sample(stubs, 2)
            u, v = random.choice(G.edges())

            if _is_valid_to_rewire(G, i, j, u, v):
                # detach u and v, link (u,i) and (v,j)
                self.log_v(
                    're-link ({0:s} {1:s}) -> ({0:s} {2:s}) ({1:s} {3:s})'
                    .format(str(u), str(v), str(i), str(j))
                )
                G.remove_edge(u,v)
                G.add_edges_from([(u,i),(v,j)])
                stubs.remove((i, si))
                stubs.remove((j, sj))

        if trials == max_trials and len(stubs) > 0:
            self.log_v(
                'optimize failed after {0:d} trials'
                .format(trials)
            )
        else:
            Rnew = R(G)
            self.log_v(
                'optimize success R = {0:3f} -> {1:3f} after {2:d} trials'
                .format(Rorig, Rnew, trials)
            )
            self._graph = G
        return self.current_graph()


# check if edge (i, j) can be added to graph G
def _is_valid_to_add(G, i, j):
    # same vertex
    if i == j: return False
    # parallel edge
    if j in G.nodes() and i in G[j] or\
       i in G.nodes() and j in G[i]: return False
    return True

# check if vertex (i, j) can be added to graph G
# whareas edge (u, v) exists
# example:
#    i   j    i   j
#          ->   X
#    u - v    u   v
def _is_valid_to_rewire(G, i, j, u, v):
    # check if same vertex
    if i in (u,v) or j in (u,v): return False
    # check if parallel edge
    if i in G[u] or j in G[v]: return False
    # simulate swap
    G.remove_edge(u,v)
    G.add_edges_from([(u,i),(v,j)])
    # then check connectivity
    can_rewire = nx.has_path(G, u, v)
    # undo
    G.add_edge(u,v)
    G.remove_edges_from([(u,i),(v,j)])
    return can_rewire
