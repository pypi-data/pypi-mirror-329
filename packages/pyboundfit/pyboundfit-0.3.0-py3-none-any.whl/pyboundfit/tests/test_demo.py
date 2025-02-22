# -*- coding: utf-8 -*-
#
# Copyright 2025 Universidad Complutense de Madrid
#
# This file is part of pyboundfit
#
# SPDX-License-Identifier: GPL-3.0+
# License-Filename: LICENSE.txt
#

import numpy as np

from pyboundfit import demo


def test_demo():
    pol1, pol2, spl1, spl2 = demo(plot=False, verbose=True)

    expected_pol1_coef = np.array([ 22.43919975,  -41.5216713,  -7.32451917,  140.23297889,
                                    41.59855497, -148.66578342])
    expected_pol2_coef = np.array([-11.22045535, -15.49805568,  -9.02210301,  62.04744721,
                                   33.22781206,  -70.98120294])
    expected_spl1_coef = np.array([ 110.36395425,  23.43548377,  42.79209189,  30.01414642,
                                    15.55226365,  19.46240421,  38.98864774,  -3.13644448,
                                    7.90421015])
    expected_spl2_coef = np.array([ 55.69534422, -27.1246286,   22.23452684, -30.93616187,
                                    4.90583046, -40.21815658,   5.94339884, -11.00589461,
                                    -8.46910007])

    assert np.all(np.isclose(pol1.coef, expected_pol1_coef))
    assert np.all(np.isclose(pol2.coef, expected_pol2_coef))
    assert np.all(np.isclose(spl1.get_coeffs(), expected_spl1_coef))
    assert np.all(np.isclose(spl2.get_coeffs(), expected_spl2_coef))
