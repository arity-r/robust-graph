from __future__ import division
import networkx as nx

from robust_graph import LOG_LEVEL_INFO as LOG_LEVEL

# s robustness
from robust_graph import R, s

# compare three algorithm
from robust_graph import Schneider
from robust_graph import WuHolme
from robust_graph import IchinoseSatotani

# useful to build graph in the paper,
# [Onion structure and network robustness]
from robust_graph import scale_free_network

# base class to optimize graph robustness
from robust_graph import Optimizer

# this optimization algorithm does nothing
# so we can calculate original graph's s(q)
class Original(Optimizer):
    def _update_one_step(self, graph):
        return True, graph

n_nodes = 100
n_graphs = 10
n_attacks = 10
filename = 'robustness_comparison.csv'
# optimizer dictionary (column -> (opt_class, log_level, force_update,
#                                  configs, steps))
optimizers = {
    'Original'  : (Original,         LOG_LEVEL, True,
                                 dict(),                1),

    'Schneider' : (Schneider,        LOG_LEVEL, True,
                                  dict(max_trials=100), 100),

    'Holme'     : (WuHolme,          LOG_LEVEL, True,
                                  dict(),                1),

    'Ichinose'  : (IchinoseSatotani, LOG_LEVEL, False,
                                  dict(greedy=True),    100)
}

result_s = dict(zip(optimizers.keys(),
                    [[0]*n_nodes]*len(optimizers)))

for _ in range(n_graphs):
    # build graph and optimize with each algorithm
    G = scale_free_network(n_nodes)

    for name, params in optimizers.items():
        opt_cls, log_level, force_update, config, steps = params
        optimizer = opt_cls(G, log_level, force_update, **config)
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
