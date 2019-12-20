# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 16:57:02 2019

@author: jankos
"""
import numpy as np
import pandas as pd
import pdb
def calc_normalization(value_counts):
#    pdb.set_trace()
    value_counts = value_counts/np.linalg.norm(value_counts.values)
#    pdb.set_trace()
    value_counts = value_counts

    return value_counts

def distance_projection(p1, p2):
    dotproj = np.dot(p1,p2.T)

    return dotproj