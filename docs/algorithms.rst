
Algorithms
==========

Schneider et al.
----------------
Class reference:
:class:`~.Schneider`

#. Select a pair of edges randomly and swap them
#. If it has higher R, accept the swapping
#. If not, try to swap again

.. seealso::

   :cite:`Schneider2011`

Configure parameters:

========== ======= =================================
Name       Default Description
========== ======= =================================
max_trials 100     The maximum number of swap trials
========== ======= =================================


Wu and Holme
------------

Class reference:
:class:`~.WuHolme`

.. note::
   Too difficult to understand. I quit.

.. seealso::
   :cite:`Holme2002`

Configure parameters:

========== ======= ==================================
Name       Default Description
========== ======= ==================================
max_trials 100     The maximum number of join process
a          3       Parameter in equation
========== ======= ==================================

Sun et al.
----------

Class reference:
:class:`~.Sun`

.. note::
   Too difficult to understand. I quit.

.. seealso::
   :cite:`Sun2016`

Configure parameters:

========== ======= ==================================
Name       Default Description
========== ======= ==================================
max_trials 100     The maximum number of join process
Ng         10      The number of neighbor solutions
Nt         6       Length of tabu list
========== ======= ==================================

Ichinose et al.
---------------
Class reference:
:class:`~.IchinoseSatotani`

This algorithm aims to improve both robustness and degree correlation.

#. For each edges, calculate difference of degrees of endpoints defined as
   :math:`\Delta_e = |k_i - k_j|`.
#. Select two edges by performing roulette selection.

   .. math::
       p_e = \frac{\Delta_e}{\sum_{f \in E}\Delta_f}

#. Perform double edge swap using selected edges.
#. (Optional) for edges :math:`(i, j)` and :math:`(u, v)` are selected,
   there are two possible results(:math:`(i, u), (j, v)` and
   :math:`(i, v), (j, u)`) from double edge swapping.
   To increase network robustness and degree correlation, select

   .. math::
       \begin{cases}
         ((i, u), (j, v)) & (\Delta1 < \Delta2) \\
         ((i, v), (j, u)) & (otherwise)
       \end{cases}

   where :math:`\Delta_1 = |k_i - k_u| + |k_j - k_v|` and
   :math:`\Delta_2 = |k_i - k_v| + |k_j - k_u|`.
#. Accept swapping if there are no self loops, parallel edges,
   and not separated by swapping.

Configure parameters:

========== ======= ====================================
Name       Default Description
========== ======= ====================================
max_trials 100     The maximum number of trials
greedy     False   If true, always choose swap
                   that makes higher degree correlation
========== ======= ====================================

