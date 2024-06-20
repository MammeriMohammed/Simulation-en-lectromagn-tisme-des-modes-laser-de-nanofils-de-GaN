#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 04:56:16 2024

@author: mohamed
"""
import numpy as np


def cutoff(mode, V):
    cutoffs = {}
    for key, value in mode.items():
        name = key 
        table = value
        L = len(table)
        for i in range(L):
            if table[i] is not None:
                cutoffs[name] = V[i]
                break
    return cutoffs
