"""
Log levels used by :class:`~.Optimizer`

===================== ====== ======================
Name                  Value  Description
===================== ====== ======================
``LOG_LEVEL_QUIET``   0      suppresses all logs
``LOG_LEVEL_ERROR``   2      shows only error logs
``LOG_LEVEL_WARNING`` 3      errors and warnings
``LOG_LEVEL_DEBUG``   4      debug information
``LOG_LEVEL_INFO``    5      useful information
``LOG_LEVEL_VERBOSE`` 7      shows all things
===================== ====== ======================

The log is formatted in csv::

    timestamp,loglevel,tag,message
    2016-05-29 22:37:54.363486,D,IchinoseSatotani,optimizer initialized (graph=<7F475B625AD0> config={'log_level': 'V'})
    2016-05-29 22:37:54.363755,D,IchinoseSatotani,enter optimization (current 0 step total 2 steps)
    2016-05-29 22:37:54.456545,V,IchinoseSatotani,select edges (9 58) and (9 83) (k = (55 4) (55 3))
    2016-05-29 22:37:54.469002,V,IchinoseSatotani,select edges (28 68) and (9 17) (k = (10 4) (55 5))
    2016-05-29 22:37:54.484720,V,IchinoseSatotani,select edges (9 42) and (9 29) (k = (55 7) (55 3))
    2016-05-29 22:37:54.497236,V,IchinoseSatotani,select edges (9 57) and (9 18) (k = (55 3) (55 4))
    2016-05-29 22:37:54.509615,V,IchinoseSatotani,select edges (9 69) and (9 12) (k = (55 3) (55 4))
    2016-05-29 22:37:54.521980,V,IchinoseSatotani,select edges (9 84) and (9 79) (k = (55 8) (55 3))
    2016-05-29 22:37:54.538531,V,IchinoseSatotani,select edges (48 55) and (3 9) (k = (3 11) (11 55))
    2016-05-29 22:37:54.550602,V,IchinoseSatotani,select edges (9 56) and (39 95) (k = (55 4) (23 3))
    2016-05-29 22:37:54.562486,V,IchinoseSatotani,select edges (9 51) and (58 63) (k = (55 4) (4 6))
    2016-05-29 22:37:54.574546,V,IchinoseSatotani,select edges (9 12) and (39 42) (k = (55 4) (23 7))
    2016-05-29 22:37:54.586598,V,IchinoseSatotani,select edges (9 64) and (9 39) (k = (55 13) (55 23))
    2016-05-29 22:37:54.600107,V,IchinoseSatotani,select edges (9 64) and (9 64) (k = (55 13) (55 13))
    2016-05-29 22:37:54.612631,V,IchinoseSatotani,select edges (9 18) and (9 22) (k = (55 4) (55 2))
    2016-05-29 22:37:54.624887,V,IchinoseSatotani,select edges (9 26) and (3 9) (k = (55 3) (11 55))
    2016-05-29 22:37:54.640989,V,IchinoseSatotani,select edges (9 53) and (84 87) (k = (55 3) (8 4))
    2016-05-29 22:37:54.653399,V,IchinoseSatotani,select edges (27 39) and (9 39) (k = (3 23) (55 23))
    2016-05-29 22:37:54.665908,V,IchinoseSatotani,select edges (9 37) and (25 86) (k = (55 4) (14 5))
    2016-05-29 22:37:54.678271,V,IchinoseSatotani,select edges (9 18) and (9 21) (k = (55 4) (55 3))
    2016-05-29 22:37:54.690589,V,IchinoseSatotani,select edges (9 62) and (9 18) (k = (55 3) (55 4))
    2016-05-29 22:37:54.702918,V,IchinoseSatotani,select edges (42 54) and (28 82) (k = (7 11) (10 3))
    2016-05-29 22:37:54.703237,V,IchinoseSatotani,swap edges (42 54) and (28 82)
    2016-05-29 22:37:54.764395,V,IchinoseSatotani,optimize success R = 0.202100 -> 0.203600 after 20 trials
    2016-05-29 22:37:54.889305,I,IchinoseSatotani,update robustness 0.196500 -> 0.199500 at 0 step
    2016-05-29 22:37:54.968138,V,IchinoseSatotani,select edges (9 77) and (7 80) (k = (55 12) (3 7))
    2016-05-29 22:37:54.968564,V,IchinoseSatotani,swap edges (9 77) and (7 80)
    2016-05-29 22:37:55.026764,V,IchinoseSatotani,optimize success R = 0.205300 -> 0.202900 after 1 trials
    2016-05-29 22:37:55.149647,I,IchinoseSatotani,update robustness 0.205300 -> 0.197600 at 1 step
    2016-05-29 22:37:55.150018,D,IchinoseSatotani,exit optimization (current 2 step total 2 steps)

"""
from __future__ import print_function

LOG_LEVEL_QUIET   = 0
LOG_LEVEL_ERROR   = 2
LOG_LEVEL_WARNING = 3
LOG_LEVEL_DEBUG   = 4
LOG_LEVEL_INFO    = 5
LOG_LEVEL_VERBOSE = 7
LOG_LEVEL_TO_LETTER_TABLE = {
    LOG_LEVEL_QUIET:   'Q',
    LOG_LEVEL_INFO:    'I',
    LOG_LEVEL_DEBUG:   'D',
    LOG_LEVEL_WARNING: 'W',
    LOG_LEVEL_ERROR:   'E',
    LOG_LEVEL_VERBOSE: 'V',
}

def print_log_header():
    """
    shows header row::

        timestamp,loglevel,tag,message
    """
    print('timestamp,loglevel,tag,message')

