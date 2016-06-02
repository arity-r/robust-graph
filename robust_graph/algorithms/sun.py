from __future__ import absolute_import
import networkx as nx
from robust_graph import R
from robust_graph import LOG_LEVEL_QUIET
from robust_graph import Optimizer

class Sun(Optimizer):
    """
    Improve network robustness with tabu search
    :cite:`Sun2016`

    .. note::
       The result from this algorithm may not accord to :cite:`Sun2016`.

    :param networkx.Graph graph: Graph to be optimized
    :param int log_level: Log level defined in
        :mod:`robust_graph.optimize.log_level`
    :param bool force_update: If True, iterates ``max_trials`` times,
        if False, continue until Gc gain a swap (updates Gc Nt times)
    :param int max_trials: The number of iteration
        (Only works ``force_udpate==True``)
    :param int Ng: The number of neighbor solutions
    :param int Nt: Length of tabu list
    """
    def __init__(self, graph,
                 log_level=LOG_LEVEL_QUIET,
                 force_update=True,
                 max_trials=1000,
                 Ng=10, Nt=6):
        super(Sun, self).__init__(
            graph, log_level, force_update,
            max_trials=max_trials, Ng=Ng, Nt=Nt)
        # the number of neighbor solutions
        self.Ng = Ng
        # size of tabu list
        self.Nt = Nt
        # the maximum number of trials
        self._max_trials = max_trials
        # tabu list
        self.TList = []
        # the number of update on TList
        self.t = 0
        # misc.
        self.Gc = graph.copy()
        self.Gbest, self.Rbest = self.Gc, R(self.Gc)

    def _update_one_step(self, graph):
        if self._force_update:
            # ignore context
            self.TList = []
            self.Gc = graph.copy()
            self.Gbest, self.Rbest = self.Gc, R(self.Gc)

        is_complete = True if self._force_update else False
        trial = 0
        while trial < self._max_trials and\
              (self._force_update or
               not self._force_update and self.t <= self.Nt):
            trial += 1

            # find best neighboring solution
            Gnew = self._find_best()
            Rnew = R(Gnew)

            self.log_v(
                'compare Gbest <{:X}> (R={:f}) and Gnew <{:X}> (R={:f}) at {:d} trial'
                .format(id(self.Gbest), self.Rbest, id(Gnew), Rnew, trial)
            )

            if Rnew > self.Rbest:

                update_log_msg = 'update R {:f} -> {:f} at {:d} trial'\
                                 .format(self.Rbest, Rnew, trial)
                if not self._force_update:
                    update_log_msg += '({:d}/{:d})'.format(self.t+1, self.Nt+1)
                else:
                    update_log_msg += '({:d} times)'.format(self.t+1)
                self.log_v(update_log_msg)

                self.Gbest, self.Rbest = Gnew, Rnew
                self.TList.append(self.Gbest)
                if len(self.TList) > self.Nt:
                    self.log_v(
                        'update Gc <{:X}> -> <{:X}> at {:d} trial'
                        .format(id(self.Gc), id(self.TList[0]), trial)
                    )
                    self.Gc = self.TList.pop(0)
                # end if
                # update the number of update on TList
                self.t += 1
                if self.t == self.Nt+1:
                    is_complete = True
            # end if
        # end while

        if not self._force_update and is_complete:
            self.t = 0

        return is_complete, self.Gbest

    def _is_matches_to_tabu(self, G):
        matches = False
        # graph comparison by comparing edge set
        for T in self.TList:
            if set(T.edges()) != set(G.edges()):
                continue

            matches = True
            self.log_v(
                'tabu match {:X} generated from {:X} and {:X} from tabu list'
                .format(id(G), id(self.Gc), id(T))
            )
            break
        return matches

    def _find_best(self):
        GList, RList = [], []
        n = 0
        self.log_v(
            'generating neighbor solution from <{:X}>'
            .format(id(self.Gc))
        )
        while n <= self.Ng:
            n += 1
            G1 = nx.double_edge_swap(self.Gc.copy())
            if self._is_matches_to_tabu(G1):
                continue

            R1 = R(G1)
            GList.append(G1)
            RList.append(R1)

        # findbest in the paper
        return max(zip(GList, RList), key=lambda t: t[1])[0]
