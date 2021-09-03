"""
Crystal Aging Project

Sigmoid functions that are used for smooth
acceleration of asperity in simulations

This project is distributed under the GNU General Public License v3.
For more information, see the LICENSE file in the top-level dictionary.
"""

def sigmoid(rel_time, rate, cutoff=100):
    """Sigmoid function where a cutoff it set to avoid
    numerical instability
    """
    from math import exp
    if rel_time < -cutoff/rate:
        return 0.
    elif rel_time > cutoff/rate:
        return 1.
    else:
        return 1./(1+exp(-rate*rel_time))


def sig_int(rel_time, rate, cutoff=100):
    """Sigmoid function integrated
    """
    from math import exp, log
    if rel_time < -cutoff/rate:
        return 0.
    elif rel_time > cutoff/rate:
        return rel_time
    else:
        return log(1+exp(rate*rel_time))/rate


def sig_inv(rel_time, rate, cutoff=100):
    """Sigmoid function inverse, 1-f(x)
    """
    from math import exp
    if rel_time < -cutoff/rate:
        return 1.
    elif rel_time > cutoff/rate:
        return 0.
    else:
        return 1-1./(1+exp(-rate*rel_time))


def sig_inv_int(time, stop, rate, cutoff=100):
    """Sigmoid function inverse integrated
    """
    from math import exp, log
    rel_time = time-stop
    if rel_time < -cutoff/rate:
        return time
    elif rel_time > cutoff/rate:
        return stop
    else:
        return time-log(1+exp(rate*rel_time))/rate
