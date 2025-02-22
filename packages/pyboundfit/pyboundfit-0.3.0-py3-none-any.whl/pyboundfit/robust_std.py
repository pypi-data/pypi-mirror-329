#
# Copyright 2025 Universidad Complutense de Madrid
#
# This file is part of pyboundfit
#
# SPDX-License-Identifier: GPL-3.0-or-later
# License-Filename: LICENSE.txt
#


import numpy as np


def robust_std(x, debug=False):
    """Compute a robust estimator of the standard deviation

    See Eq. 3.36 (page 84) in Statistics, Data Mining, and Machine
    in Astronomy, by Ivezic, Connolly, VanderPlas & Gray

    Parameters
    ----------
    x : 1d numpy array, float
        Array of input values which standard deviation is requested.
    debug : bool
        If True prints computed values

    Returns
    -------
    sigmag : float
        Robust estimator of the standar deviation
    """

    x = np.asarray(x)

    # compute percentiles and robust estimator
    q25 = np.percentile(x, 25)
    q75 = np.percentile(x, 75)
    sigmag = 0.7413 * (q75 - q25)

    if debug:
        print('debug|sigmag -> q25......................:', q25)
        print('debug|sigmag -> q75......................:', q75)
        print('debug|sigmag -> Robust standard deviation:', sigmag)

    return sigmag
