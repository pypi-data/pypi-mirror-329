#
# This file is part of pyboundfit
#
# SPDX-License-Identifier: GPL-3.0+
# License-Filename: LICENSE.txt
#

"""Numerical spline fit using different strategies."""

from scipy.interpolate import LSQUnivariateSpline


def fun_residuals_spl(params, xnor, ynor, w, bbox, k, ext):
    """Compute residuals of spline fit
    """

    spl = LSQUnivariateSpline(
        x=xnor,
        y=ynor,
        t=[item.value for item in params.values()],
        w=w,
        bbox=bbox,
        k=k,
        ext=ext,
        check_finite=False
    )
    return spl.get_residual()
