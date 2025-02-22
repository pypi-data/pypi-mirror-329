#
# Copyright 2025 Universidad Complutense de Madrid
#
# This file is part of pyboundfit
#
# SPDX-License-Identifier: GPL-3.0+
# License-Filename: LICENSE.txt
#

import numpy as np
from numpy.polynomial import Polynomial

from .robust_std import robust_std


def boundfit_poly(
        x, y, deg, boundary='upper',
        xi=10, niter=100,
        expweight=False,
        return_all_fits=False
):
    if boundary not in ['upper', 'lower']:
        raise SystemExit(f'Invalid boundary: {boundary}')

    flag = {'upper': 1, 'lower': -1}

    npoints = len(x)
    if len(y) != npoints:
        raise ValueError(f'{len(x)=} != {len(y)=}')

    # initial fit
    poly = Polynomial.fit(x=x, y=y, deg=deg)
    poly.niter = 0

    # residuals and robust standard deviation
    if expweight:
        residuals = y - poly(x)
        sigmag = robust_std(residuals)
    else:
        sigmag = 1

    # list with all the fits
    if return_all_fits:
        list_all_fits = [poly]
    else:
        list_all_fits = None

    # iterate to compute boundary
    residuals_norm_previous = None
    for i in range(niter):
        residuals_norm = (y - poly(x)) / sigmag
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
        poly = Polynomial.fit(x=x, y=y, deg=deg, w=w)
        poly.niter = i + 1
        if return_all_fits:
            list_all_fits.append(poly)
        if i == 0:
            residuals_norm_previous = residuals_norm
        else:
            if np.all(np.isclose(residuals_norm, residuals_norm_previous)):
                break
            else:
                residuals_norm_previous = residuals_norm

    if return_all_fits:
        return poly, list_all_fits
    else:
        return poly
