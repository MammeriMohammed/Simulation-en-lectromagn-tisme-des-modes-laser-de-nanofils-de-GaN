#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 01:48:59 2024

@author: mohamed
"""

import numpy as np

def dichotomy(func, lo, hi, args=(), tol=1e-5, max_iter=100):
    for _ in range(max_iter):
        mid = (lo + hi) / 2
        f_lo = func(lo, *args)
        f_mid = func(mid, *args)

        if f_mid == 0 or (hi - lo) / 2 < tol:
            return mid
        if np.sign(f_mid) == np.sign(f_lo):
            lo = mid
        else:
            hi = mid

    return (lo + hi) / 2

