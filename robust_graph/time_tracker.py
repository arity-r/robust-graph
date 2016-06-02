from __future__ import print_function
from datetime import datetime
from .log_level import *
from .optimizer import Optimizer

class TimeTracker(object):
    """
    TimeTracker constructor

    :param Optimizer opt_class: Optimization algorithm
    :param networkx.Graph graph: Graph to be optimized
    :param list-of-tuple cols: List of column name and function(graph -> double)
    :param dict config: Optional parameters for optimizer
    """
    def __init__(self, opt_class, graph, cols=[], **config):
        self._optimizer = opt_class(graph, **config)
        self._cols = cols

        # the following add log_e, log_w, log_d, log_i, log_v
        for log_level, log_letter in LOG_LEVEL_TO_LETTER_TABLE.items():
            log_function_name = 'log_%s'%log_letter.lower()
            setattr(self,
                    log_function_name,
                    getattr(self._optimizer, log_function_name)
            )

        self.log_d('tracker initialized')
        self.log_d('tracker adding 0th row...')
        # add first row
        self._rows = []
        self._rows.append(self._make_row())

    def _make_header(self):
        """
        Create header row
        """
        row = ['step']
        row.extend(map(lambda c: c[0], self._cols))
        return row

    def _make_row(self):
        """
        Create current row
        """
        row = [self._optimizer.current_step()]
        row.extend(map(lambda c: c[1](self._optimizer.current_graph()),
                       self._cols))
        return row

    def track(self, steps):
        """
        Run simulation on :class:`~.Optimizer` and store results on every steps.

        :param int steps: Simulation step on :class:`~.Optimizer`
        """
        ordering = lambda n: '%d%s'%(n,'tsnrhtdd'[(n/10%10!=1)*(n%10<4)*n%10::4])
        self.log_d('tracking started (total {0:d} steps)'
                   .format(steps))
        start_step = self._optimizer.current_step()
        while self._optimizer.current_step() - start_step < steps:
            self._optimizer.optimize(steps=1)
            self.log_d('tracker adding {:s} row'
                       .format(ordering(self._optimizer.current_step()))
            )
            self._rows.append(self._make_row())
        self.log_d('tracking finished (total {0:d} steps)'
                   .format(steps))

    def rawdata(self):
        """
        Obtain tracker result as a dictionary

        :return: Dictionary (key = column names, values = column data)
        :rtype: dict
        """
        return dict(zip(
            map(lambda c: c[0], self._cols),
            list(zip(*self._rows))[1:]))

    def dumps(self):
        """
        Dump result as a csv string.

        :return: Tracking result in csv format
        :rtype: str
        """
        csv_table = [self._make_header()] +\
                    map(lambda r: map(str, r), self._rows)
        csv_text = '\n'.join(map(lambda r: ','.join(r), csv_table))
        return csv_text

    def dump(self, filename):
        """
        Dump result to file as csv format

        :param str filename: Filename
        """
        with open(filename, 'w') as fp:
            fp.write(self.dumps())

    def current_step(self):
        """
        Returns the number of current steps.

        :return: Current step
        :rtype: int
        """
        return self._optimizer.current_step()

    def current_graph(self):
        """
        Returns a deep copy of graph which this tracker holds currently.

        :return: Current graph of tracker
        :rtype: networkx.Graph
        """
        return self._optimizer.current_graph()

