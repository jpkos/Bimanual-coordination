# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 17:19:56 2019

@author: jankos
"""

import unittest
import numpy as np
import pandas as pd
#%%

def fun(x):
    return x + 3

class TestTest(unittest.TestCase):
    def test1(self):
        self.assertEqual(fun(5), 10)

if __name__=='__main__':
    unittest.main()