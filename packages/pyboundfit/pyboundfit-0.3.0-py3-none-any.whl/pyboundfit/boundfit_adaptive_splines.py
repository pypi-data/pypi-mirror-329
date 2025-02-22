#
# Copyright 2025 Universidad Complutense de Madrid
#
# This file is part of pyboundfit
#
# SPDX-License-Identifier: GPL-3.0+
# License-Filename: LICENSE.txt
#

"""Compute boundary using adaptive splines"""

import numpy as np
from .numsplines import AdaptiveLSQUnivariateSpline
from .robust_std import robust_std


def remove_close_knots(xknots, threshold=1E-3):
    """Remove colliding knots from xknots.
    """
    filtered_xknots = []
    mininum_distance = threshold * (xknots[-1] - xknots[0])
    for value in xknots:
        if all(abs(value - x) > mininum_distance for x in filtered_xknots):
            filtered_xknots.append(value)
    filtered_xknots = np.array(filtered_xknots)
    return filtered_xknots


def boundfit_adaptive_splines(
        x, y, t, boundary='upper',
        xi=10, niter=100,
        expweight=False,
        adaptive=False,
        return_all_fits=False
):
    """When adaptive=True, close knots are merged!
    """
    if boundary not in ['upper', 'lower']:
        raise SystemExit(f'Invalid boundary: {boundary}')

    flag = {'upper': 1, 'lower': -1}

    npoints = len(x)
    if len(y) != npoints:
        raise ValueError(f'{len(x)=} != {len(y)=}')

    # the x data must be sorted
    isort = np.argsort(x)
    x = x[isort]
    y = y[isort]
    # initial fit
    spl = AdaptiveLSQUnivariateSpline(x=x, y=y, t=t, adaptive=False)
    spl.niter = 0
    spl.xi = xi

    # residuals and robust standard deviation
    if expweight:
        residuals = y -spl(x)
        sigmag = robust_std(residuals)
    else:
        sigmag = 1

    # list with all the fits
    if return_all_fits:
        list_all_fits = [spl]
    else:
        list_all_fits = None

    # iterate to refine boundary
    residuals_norm_previous = None
    for i in range(niter):
        t_previous = spl.get_knots()[1:-1]  # remove first and last knots to keep the inner knots
        t = remove_close_knots(t_previous)
        residuals_norm = (y - spl(x)) / sigmag
        if boundary == 'upper':
            fraction_points = np.sum(residuals_norm < 0) / npoints
        else:
            fraction_points = np.sum(residuals_norm > 0) / npoints
        if expweight:
            w = np.exp(flag[boundary] * xi * residuals_norm * fraction_points)
        else:
            sign = np.sign(residuals_norm).astype(int)
            w = np.ones_like(x)
            w[sign==flag[boundary]] = xi * fraction_points
            w[sign==0] = xi * fraction_points
        spl = AdaptiveLSQUnivariateSpline(x=x, y=y, w=w, t=t, adaptive=adaptive)
        spl.niter = i + 1
        spl.xi = xi
        if return_all_fits:
            list_all_fits.append(spl)
        # stop iterations when knot location and residuals are stable
        if i == 0:
            residuals_norm_previous = residuals_norm
        else:
            if np.all(np.isclose(residuals_norm, residuals_norm_previous)):
                break
            else:
                residuals_norm_previous = residuals_norm

    if return_all_fits:
        return spl, list_all_fits
    else:
        return spl
