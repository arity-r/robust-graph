from __future__ import division
import networkx as nx


# R robustness and s robustness
from robust_graph import R, s

# log level: use LOG_LEVEL_DEBUG or LOG_LEVEL_VERBOSE
#            to get more information
#            use LOG_LEVEL_QUIET to suppress all log
from robust_graph import LOG_LEVEL_INFO as LOG_LEVEL
#from robust_graph.optimize import LOG_LEVEL_VERBOSE as LOG_LEVEL

# opt. algorithms: see /robust_graph/optimize/algorithm
from robust_graph import Schneider
from robust_graph import WuHolme
from robust_graph import Sun
from robust_graph import IchinoseSatotani

# class to optimize graph robustness
from robust_graph import Optimizer

# useful to build graph in the paper,
# [Onion structure and network robustness]
from robust_graph.util import scale_free_network

"""
this optimization algorithm does nothing
so we can calculate original graph's s(q)
"""
class Original(Optimizer):
    def _update_one_step(self, graph):
        return True, graph

n_nodes = 10
n_graphs = 1
n_attacks = 1
filename = 'result.csv'
# optimizer dictionary (column -> (opt_class, log_level, force_update,
#                                  configs, steps))
optimizers = {
    'original'            : (Original,         LOG_LEVEL, True,
                             dict(),               1),

    'schneider 100 swaps' : (Schneider,        LOG_LEVEL, True,
                             dict(max_trials=100), 100),

    'schneider 1000 swaps': (Schneider,        LOG_LEVEL, True,
                             dict(max_trials=100), 1000),

    'wu holme'            : (WuHolme,          LOG_LEVEL, False,
                             dict(a=3),            1),

    'ichinose 100 swaps'  : (IchinoseSatotani, LOG_LEVEL, False,
                             dict(),               100),

    'ichinose 1000 swaps' : (IchinoseSatotani, LOG_LEVEL, False,
                             dict(),               1000),

    'ichinose greedy 100 swaps': (IchinoseSatotani, LOG_LEVEL, False,
                                  dict(greedy=True), 100)
}

result_s = dict(zip(optimizers.keys(),
                    [[0]*n_nodes]*len(optimizers)))

for _ in range(n_graphs):
    # build graph and optimize with each algorithm
    G = powerlaw_graph_in_wu(n_nodes)
    for name, v in optimizers.items():
        optimizer, log_level, force_update, config, steps = v
        # set log level imported on the top
        optimizer = optimizer(G, log_level, force_update, **config)
        optimized = optimizer.optimize(steps)
        # the following three lines do:
        #    s[name] += s(optimized) * n_attacks
        result_s[name] = map(sum,
            zip(result_s[name],
                map(lambda e: e*n_attacks, s(optimized, n=n_attacks))))

# convert result_s sum of s(q) -> average of s(q)
for k, v in result_s.items():
    result_s[k] = map(lambda s: s / (n_graphs*n_attacks), v)

# build csv text with header column (q)
csvtxt = 'q,'+','.join(result_s.keys()) + '\n' +\
         '\n'.join(map(lambda l: '%d,'%l[0]+','.join(map(str, l[1])),
                       enumerate(zip(*result_s.values()), 1)
         ))

with open(filename, 'w') as fp:
    fp.write(csvtxt)
