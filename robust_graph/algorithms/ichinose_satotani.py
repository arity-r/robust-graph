from __future__ import division, absolute_import
import random
import networkx as nx
from robust_graph import R
from robust_graph import LOG_LEVEL_QUIET, LOG_LEVEL_VERBOSE
from robust_graph import Optimizer

class IchinoseSatotani(Optimizer):
    """
    Improve network robustness with degree correlation

    :param networkx.Graph graph: Graph to be optimized
    :param int log_level: Log level defined in :mod:`robust_graph.optimize.log_level`
    :param bool force_update: If True, accept update even if :func:`~_update_one_step` claims imcomplete result
    :param int max_trials: The maximum number of trials for swapping
    :param bool greedy: Choose higher degree correlation swap
    """
    def __init__(self, graph,
                 log_level=LOG_LEVEL_QUIET,
                 force_update=True,
                 max_trials=100,
                 greedy=False):
        super(IchinoseSatotani, self).__init__(
            graph, log_level, force_update,
            max_trials=max_trials, greedy=greedy)

    def _update_one_step(self, G):
        max_trials = self._config['max_trials']
        is_greedy = self._config['greedy']

        if self._log_level == LOG_LEVEL_VERBOSE: # HACK
            Rorig = R(G)

        trials = 0
        is_success = False
        while trials < max_trials:
            trials += 1
            (u,v), (x,y) = _select_edges(G, is_greedy)

            self.log_v(
                'select edges '+\
                '({:s} {:s}) and ({:s} {:s}) '
                .format(*map(str, (u, v, x, y)))+\
                '(k = ({:d} {:d}) ({:d} {:d}))'
                .format(*map(G.degree, (u, v, x, y)))
            )

            if _is_valid_to_swap(G, u, v, x, y):
                G.remove_edges_from([(u,v),(x,y)])
                G.add_edges_from([(u,x),(v,y)])
                self.log_v(
                    'swap edges '+\
                    '({:s} {:s}) and ({:s} {:s}) '
                    .format(*map(str, (u, v, x, y)))
                )

                is_success = True
                break

        if is_success:
            if self._log_level == LOG_LEVEL_VERBOSE: # HACK
                Rnew = R(G)
                self.log_v(
                    'optimize success R = {0:3f} -> {1:3f} after {2:d} trials'
                    .format(Rorig, Rnew, trials)
                )
        else:
            self.log_v(
                'optimize failed after {0:d} trials'
                .format(trials)
            )
        return is_success, G


def _select_edges(G, is_greedy):
    kdelta = lambda e: abs(G.degree(e[0])-G.degree(e[1]))
    deg_diff = dict(zip(G.edges_iter(),
                        map(kdelta, G.edges_iter())))
    # choose two links from degree difference
    selected_edges = []
    for __ in range(2):
        prob_total = 0
        rvalue = random.uniform(0, sum(deg_diff.values()))
        for key, value in deg_diff.items():
            prob_total += value
            if rvalue < prob_total:
                selected_edges.append(key)
                break
    (u,v), (x,y) = selected_edges
    # if greedy, select higher-degree-correlation rewiring
    if is_greedy:
        if kdelta((u,x))+kdelta((v,y)) > kdelta((u,y))+kdelta((v,x)):
            x,y = y,x
    else:
        #if random.uniform(0, 1) < 0.5: # two swap results from 4 nodes
        if False: # see networkx.double_edge_swap
            x,y = y,x
    return (u, v), (x, y)

def _is_valid_to_swap(G, u, v, x, y):
    # check if same vertex
    if x in (u,v) or y in (u,v): return False
    # check if parallel edge
    if x in G[u] or y in G[v]: return False

    # simulate swap
    G.remove_edges_from([(u,v),(x,y)])
    G.add_edges_from([(u,x),(v,y)])
    # then check connectivity
    can_swap = nx.has_path(G, u, v)
    # undo swapping
    G.add_edges_from([(u,v),(x,y)])
    G.remove_edges_from([(u,x),(v,y)])
    return can_swap
