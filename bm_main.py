# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 17:48:06 2019

@author: jankos
"""
import pandas as pd
import bm_analysis as ba
import helpers as bm
import config as con
from importlib import reload
#%%reload
# reload(bm)
# reload(ba)
# reload(con)
#%%Load data
dropped = ['pick/needle visible', 'touch edge', 'pierce start',
          'needle push start', 'extraction start', 'thread handling start']
participants_dict = bm.load_participants(participants_list=[x.upper() for x in con.participants],
                                         path=con.segment_annotations_path,
                                         drop_segments=dropped)
dfs_dict = bm.load_data([x.upper() for x in con.participants], sutures_list=[1,2,3,4,5],
                        path=con.actual_data_path, filename='{}_both_hands_{}_suture')
#%%Map segment labels to frames
ba.add_segments(dfs_dict, participants_dict)

#%%Classify actions
classifier = bm.Action_classifier()
for (participant, suture), df in dfs_dict.items():
    classified = classifier.classify_df_action(data=df)
    melted = pd.concat([classified.melt(value_name='action_class')])
    df['action_class'] = melted['action_class']

#%%Calculate ratios
segment_ratios_df = ba.calc_label_ratios(dfs_dict)

#%%Calculate suture bimanual and suturing efficiencies
suture_eff_df = ba.calc_suture_efficiencies(dfs_dict)

#%%Add uwomsa scores to same DF as ratios
uwomsas = pd.read_csv(con.uwomsa_path)
ba.add_uwomsa_scores(suture_eff_df, uwomsas)

#%%Calculate segment efficiencies
segment_eff_df = ba.calc_segment_efficiencies(dfs_dict)

#%%Original data has some missing vals
# ba.fix_seg_eff(segment_eff_df)

#%%Calculate similarities
sim_df = ba.calc_similarities(segment_ratios_df)
sim_df['skill_compared_to'] = sim_df['p_compared_to'].map(con.skill_map)
#%%Reshape
skill_reshaped = ba.sim_suture_reshape(sim_df)

#%%Classify by suture similarity
suture_skill_counts = ba.sim_suture_classification(skill_reshaped)

#%%Classify by segment (averaged segments)
avsegment_skill_counts = ba.sim_avsegment_classification(sim_df)

#%%Classify by segment (non-averaged segments)
segment_skill_counts = ba.sim_segment_classification(sim_df)

