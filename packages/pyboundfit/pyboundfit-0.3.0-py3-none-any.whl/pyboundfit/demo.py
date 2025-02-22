# -*- coding: utf-8 -*-
#
# Copyright 2025 Universidad Complutense de Madrid
#
# This file is part of pyboundfit
#
# SPDX-License-Identifier: GPL-3.0+
# License-Filename: LICENSE.txt
#

import matplotlib.pyplot as plt
import numpy as np

from pyboundfit import boundfit_adaptive_splines, boundfit_poly
from pyboundfit import demo


def __demofun_pol1(xtest, ytest, verbose):
    if verbose:
        print('Computing upper boundary (polynomial fit)... ', end='')
    pol1 = boundfit_poly(x=xtest, y=ytest, deg=5, boundary='upper')
    if verbose:
        print('OK!')
    return pol1

def __demofun_pol2(xtest, ytest, verbose):
    if verbose:
        print('Computing lower boundary (polynomial fit)... ', end='')
    pol2 = boundfit_poly(x=xtest, y=ytest, deg=5, boundary='lower')
    if verbose:
        print('OK!')
    return pol2

def __demofun_spl1(xtest, ytest, verbose):
    if verbose:
        print('Computing upper boundary (adaptive splines fit)... ', end='')
    spl1 = boundfit_adaptive_splines(x=xtest, y=ytest, t=5, boundary='upper', xi=100, niter=100, adaptive=False)
    if verbose:
        print('OK!')
    return spl1

def __demofun_spl2(xtest, ytest, verbose):
    if verbose:
        print('Computing lower boundary (adaptive splines fit)... ', end='')
    spl2 = boundfit_adaptive_splines(x=xtest, y=ytest, t=5, boundary='lower', xi=100, niter=100, adaptive=False)
    if verbose:
        print('OK!')
    return spl2

def __demofun(xtest, ytest, plot=False, verbose=True):
    """Compute boundaries to demo data."""
    poly1 = __demofun_pol1(xtest, ytest, verbose)
    poly2 = __demofun_pol2(xtest, ytest, verbose)
    spl1 = __demofun_spl1(xtest, ytest, verbose)
    spl2 = __demofun_spl2(xtest, ytest, verbose)

    if plot:
        xmin = np.min(xtest)
        xmax = np.max(xtest)
        xplot = np.linspace(xmin, xmax, 1000)

        fig, ax = plt.subplots()
        ax.plot(xtest, ytest, 'ko', markersize=5, label='original data')
        ax.plot(xplot, poly1(xplot), 'b-', label='polynomial fit')

        ax.plot(xplot, poly2(xplot), 'b-')

        ax.plot(xplot, spl1(xplot), 'r:', label='spline fit')
        xknots = spl1.get_knots()
        yknots = spl1(xknots)
        ax.plot(xknots, yknots, 'g.', markersize=5, label='knot location')

        ax.plot(xplot, spl2(xplot), 'r:')
        xknots = spl2.get_knots()
        yknots = spl2(xknots)
        ax.plot(xknots, yknots, 'g.', markersize=5)

        ax.fill_between(xplot, spl1(xplot), spl2(xplot), facecolor='grey', alpha=0.5)

        ax.set_xlabel('X axis (arbitrary units)')
        ax.set_ylabel('Y axis (arbitrary units)')
        ax.legend()

        plt.tight_layout()
        plt.show()

    return poly1, poly2, spl1, spl2


if __name__ == '__main__':
    pol1, pol2, spl1, spl2 = demo(plot=True, verbose=True)
    print(pol1.coef)
    print(pol2.coef)
    print(spl1.get_coeffs())
    print(spl2.get_coeffs())
