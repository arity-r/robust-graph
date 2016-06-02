from __future__ import absolute_import
import sys
from datetime import datetime
from robust_graph import R
from .log_level import *

class Optimizer(object):
    """
    Abstract class of robust-optimize algorithm

    :param networkx.Graph graph: Graph to be optimized
    :param int log_level: Log level defined in :mod:`robust_graph.optimize.log_level`
    :param bool force_update: If True, accept update even if :func:`~_update_one_step` claims imcomplete result
    :param dict config: Optional parameters on subclass

    .. automethod:: _update_one_step
    """
    def __init__(self, graph,
                 log_level=LOG_LEVEL_QUIET,
                 force_update=True,
                 **config):
        self._graph = graph.copy()
        self._config = config
        self._step = 0
        self._log_level = log_level
        self._force_update = force_update
        # the followings add log_e, log_w, log_i, log_d, log_v
        for log_level, log_letter in LOG_LEVEL_TO_LETTER_TABLE.items():
            log_function_name = 'log_%s'%log_letter.lower()
            setattr(self,
                    log_function_name,
                    self._generate_log_print(log_level)
            )

        # temporary dictionary stores log_level as letter
        _log_level = LOG_LEVEL_TO_LETTER_TABLE[self._log_level]
        self.log_d('optimizer initialized ('+\
                   'graph=<{:X}>'.format(id(graph))+\
                   'log_level={:s}'.format(_log_level)+\
                   'force_update={:s}'.format(str(force_update))+\
                   'config={:s}'.format(str(config))+\
                   ')')

    def current_graph(self):
        """
        Returns a deep copy of graph which this optimizer holds currently.

        :return: Current graph of optimizer
        :rtype: networkx.Graph
        """
        return self._graph.copy()

    def current_step(self):
        """
        Returns the number of current steps.

        :return: Current step
        :rtype: int
        """
        return self._step

    def optimize(self, steps=1):
        """
        Optimize robustness of graph.

        :param int steps: The number of optimize steps
        :return: Optimized graph in robustness
        :rtype: networkx.Graph
        """
        if steps < 0:
            self.log_e('steps cannot be negative value')

        n_steps = steps

        self.log_d(
            'enter optimization '+\
            '(current {0:d} step total {1:d} steps)'
            .format(self.current_step(), n_steps)
        )

        while steps:
            success, optimized_graph = self._update_one_step(
                self.current_graph())

            # if update failed and don't want to accept failure:
            if not success and not self._force_update:
                self.log_i(
                    'update failed at {0:d} step'
                    .format(self.current_step())
                )
                continue

            currentR = R(self.current_graph())
            newR = R(optimized_graph)
            self.log_i(
                'update robustness {0:3f} -> {1:3f} at {2:d} step'
                .format(currentR, newR, self.current_step())
            )

            self._graph = optimized_graph
            self._step += 1
            steps -= 1

        self.log_d(
            'exit optimization '+\
            '(current {0:d} step total {1:d} steps)'
            .format(self.current_step(), n_steps)
        )
        return self.current_graph()

    def _update_one_step(self, graph):
        """
        Optimize(update) robustness only one step.
        This function is not implemented and overwrite it in subclass.

        This function must return a 2-element tuple that has:

        #. represents wheather this update is complete or not
        #. optimized graph

        :param networkx.Graph graph: Graph to be optimized
        :return: Tuple described as above
        :rtype: tuple
        """
        raise NotImplementedError()

    def _generate_log_print(self, log_level):
        """
        Generate function that prints log output

        :param int log_level: Log level defined in
        :module:`~.optimize.log_level`.
        :return: Log print function
        """
        if not log_level in LOG_LEVEL_TO_LETTER_TABLE:
            raise ValueError('inadequate log level: ' + log_level)
        def log_print(msg):
            if self._log_level >= log_level:
                print(','.join([str(datetime.now()),
                                LOG_LEVEL_TO_LETTER_TABLE[log_level],
                                type(self).__name__,
                                msg]))
                if log_level == LOG_LEVEL_ERROR:
                    print('exit program by error')
                    sys.exit(1)

        return log_print
