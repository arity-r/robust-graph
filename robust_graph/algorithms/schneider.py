from __future__ import absolute_import
import networkx as nx
from robust_graph import R
from robust_graph import LOG_LEVEL_QUIET
from robust_graph import Optimizer

class Schneider(Optimizer):
    """
    Improve network robustness by comparing R
    :cite:`Schneider2011`

    :param networkx.Graph graph: Graph to be optimized
    :param int log_level: Log level defined in
        :mod:`robust_graph.optimize.log_level`
    :param bool force_update: If True, accept update
        even if :func:`~_update_one_step` claims imcomplete result
    :param int max_trials: The maximum number of trials for swapping
    """
    def __init__(self, graph,
                log_level=LOG_LEVEL_QUIET,
                 force_update=True,
                 max_trials=100):
        super(Schneider, self).__init__(
            graph, log_level, force_update,
            max_trials=max_trials)

    def _update_one_step(self, G):
        max_trials = self._config['max_trials']

        success = False
        Gorig, Rorig = G, R(G)
        Gnew, Rnew = Gorig, Rorig

        trials = 0
        while trials != max_trials:
            trials += 1
            Gnew = nx.double_edge_swap(Gorig.copy())
            Rnew = R(Gnew)
            self.log_v(
                'compare R ({0:3f} and {1:3f} at {2:d} trial)'
                .format(Rorig, Rnew, trials)
            )
            if Rnew > Rorig:
                success = True
                break

        if success:
            self.log_v(
                'optimize success R = {0:3f} -> {1:3f} after {2:d} trials'
                .format(Rorig, Rnew, trials)
            )
        else:
            self.log_v(
                'optimize failed after {0:d} trials'
                .format(trials)
            )
        return success, Gnew

