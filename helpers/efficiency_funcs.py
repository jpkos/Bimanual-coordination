# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 16:57:02 2019

@author: jankos
"""
import numpy as np
import pandas as pd

def surg_efficiency(df):
    useful = len(df[df != 'NTR'])
    total = len(df)
    if total == 0:
        return 0
    else:
        return useful/total

def bcs_ratio(bcs):
    """Calculate Balanced and master/slave ratios"""
    balanced = len(bcs[bcs == 'balanced'])
    master_slave = len(bcs[bcs.isin(['master', 'slave'])])
    total = len(bcs)
    if total == 0:
        return (np.nan, np.nan)
    bcs_ratio = np.round((balanced + master_slave)/total,4)
    ms_ratio = np.round(master_slave/total,4)

    return (bcs_ratio, ms_ratio)