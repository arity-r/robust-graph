from robust_graph import R
from robust_graph import LOG_LEVEL_INFO as LOG_LEVEL
from robust_graph import TimeTracker

# compare two algorithms
from robust_graph import Schneider, IchinoseSatotani

# function to load US airline network
from robust_graph.util import load_us

# some important constants
n_attacks = 10
n_steps = 100
fileprefix = 'speed_test'
graph = load_us()

# define columns in csv
columns = [
    # R robustness
    ('R', lambda G: R(G, n_attacks))
]

for params in [(Schneider, dict(log_level=LOG_LEVEL, force_update=True)),
               (IchinoseSatotani, dict(log_level=LOG_LEVEL,
                                       force_update=False,
                                       greedy=True))]:
    opt_cls, config = params
    tracker = TimeTracker(opt_cls, graph, columns,**config)
    tracker.track(steps=n_steps)
    tracker.dump(fileprefix + '.' + opt_cls.__name__ + '.csv')
