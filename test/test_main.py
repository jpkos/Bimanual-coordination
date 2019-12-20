# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 18:16:20 2019

@author: jankos
"""
import pandas as pd
import numpy as np
import src.helpers as bm
import src.bm_analysis as ba
from importlib import reload
#Load data
df1 = pd.read_csv('df1_test_data.csv')
df2 = pd.read_csv('df2_test_data.csv')
dfs_dict = {('Px1', 1):df1, ('Px2', 1):df2}

#%% Classify
classifier = bm.Action_classifier()
for (participant, suture), df in dfs_dict.items():
    classified = classifier.classify_df_action(data=df)
    melted = pd.concat([classified.melt(value_name='action_class')])
    df['action_class'] = melted['action_class']


#%% ratios
segment_ratios_df = ba.calc_label_ratios(dfs_dict)

#%% suture efficiencies
suture_eff_df = ba.calc_suture_efficiencies(dfs_dict)

#%% segment efficiencies
segment_eff_df = ba.calc_segment_efficiencies(dfs_dict)

#%% similarities
reload(ba)
sim_df = ba.calc_similarities(segment_ratios_df)
