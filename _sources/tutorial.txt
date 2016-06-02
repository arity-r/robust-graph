
Tutorial
========

:class:`~.Optimizer` usage
--------------------------

:class:`~.Optimizer` is a framework of robustness optimize simulation.
Algorithm is implemented in a subclass of :class:`Optimizer` (e.g.
:class:`~.Schneider` and :class:`~.IchinoseSatotani`.)

To create Optimizer object, you have to give

#. :class:`networkx.Graph` object
#. Log level defined in :mod:`~.log_level`
#. Force update flag: accept update even if it is incomplete
#. Configuration parameters, see :class:`~.Optimzier` and its subclasses

For example (using :class:`~.Schneider`),

.. code-block:: python
   
   optimizer = Schneider(graph,
                         log_level=LOG_LEVEL_INFO,
                         force_update=True,
                         max_trials=300)

After initialization has done, you can see

* How many optimization steps are passed
* What is a graph that optimizer holds currently

.. code-block:: python

   print optimizer.current_step()
   print optimzier.current_graph()

It's time to optimize the graph.
Call :meth:`optimize` to increase robustness.

.. code-block:: python

   optimizer.optimize(steps=100)

Finally, you can see how robustness is increased.

.. code-block:: python

   from robust_graph import R
   print R(optimizer.current_graph())
                

:class:`~.TimeTracker` usage
----------------------------

:class:`~.TimeTracker` is useful if you want

* see how fast is increment of robustness
* compare increment of robustness and degree correlation

To initialize :class:`TimeTracker` object, you have to give

* Subclass of :class:`~.Optimizer`
* Graph to be optimized
* Graph measurements list

.. code-block:: python

   from robust_graph import R
   import networkx.degree_pearson_correlation_coefficient as \
   degree_correlation

   cols = [('R', R),                  # R robustness
           ('r', degree_correlation), # r degree correlation
          ]

   tracker = TimeTracker(Schneider, G, cols)

After initialization, you can run optimization

.. code-block:: python

   tracker.track(steps=2)

After optimization is done, make string of csv or save it to file.

.. code-block:: python

   print tracker.dumps()
   tracker.dump('result.csv')

The result from :meth:`dumps` would be like::

   step,R,r
   0,0.20966,-0.145164333337
   1,0.20934,-0.145164333337
   2,0.21567,-0.146778584336

Also, you can use following methods

.. code-block:: python

   tracker.current_graph()
   tracker.current_step()


Custom Optimizer
----------------

.. note::
   Lack of eagerness. I write if someone insists.

