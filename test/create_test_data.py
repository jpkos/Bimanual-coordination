# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 16:44:51 2019

@author: jankos
"""
import numpy as np
import pandas as pd
from helpers.biman_helpers import create_value_count_df
from helpers.similarity_funcs import calc_normalization
from helpers.segment_mapper import Segment_mapper



def create_random_labels(framerange, act_list, target_list, n_labels):
    frames = np.sort(np.random.choice(np.arange(framerange[0], framerange[1]),
                                      n_labels, replace=False))
    activities = np.random.choice(act_list, n_labels)
    targets = np.random.choice(target_list, n_labels)

    return pd.DataFrame({'frame':frames, 'event':activities, 'target':targets})

def create_random_segments(framerange, segment_list):
    frames = np.sort(np.random.choice(np.arange(framerange[0], framerange[1]),
                                      len(segment_list), replace=False))
    frames[0] = framerange[0]-1
    frames = np.append(frames, framerange[1])
    # return pd.DataFrame({'action':segment_list, 'frame':frames})
    return (segment_list, frames)

def create_test_df(LH_actions, RH_actions):
    lh_task, lh_target = LH_actions
    rh_task, rh_target = RH_actions
    lh_event_target = ['{}:{}'.format(task,target) for task,
                          target in zip(lh_task, lh_target)]
    rh_event_target = ['{}:{}'.format(task,target) for task,
                          target in zip(rh_task, rh_target)]

    df = pd.DataFrame({'frame':[x for x in range(1,len(lh_task)+1)]*2,
                    'event':lh_task+rh_task,
                    'target':lh_target+rh_target,
                    'event:target':lh_event_target+rh_event_target,
                    'hand':['LH']*len(lh_task) + ['RH']*len(rh_task)})
    return df


#%% DF1 (Efficiency 1 for LH and RH everywhere)
segments = ['A','B']
frames = [1, 4, 6]
df1_lh_task = ['move']*3 + ['grab']*3
df1_lh_target = ['thread']*6

df1_rh_task = ['grab']*3 + ['move']*3
df1_rh_target = ['needle']*6

df1 = create_test_df((df1_lh_task, df1_lh_target), (df1_rh_task,df1_rh_target))

segmapper1 = Segment_mapper(frames,
                           segments)
segmapper1.map_segments(df1['frame'])
df1['segment'] = segmapper1.mapped
df1.to_csv('df1_test_data.csv')
#%% DF2 (should have similarity 0 with DF1 RH and similarity 1 with DF1 LH)
#Efficiency 1 for LH, 0 for RH
df2_lh_task = df1_lh_task
df2_lh_target = df1_lh_target
df2_rh_task = ['hold still']*6
df2_rh_target = ['NT']*6

df2 = create_test_df((df2_lh_task, df2_lh_target), (df2_rh_task,df2_rh_target))


segmapper2 = Segment_mapper(frames,
                           segments)
segmapper2.map_segments(df1['frame'])
df2['segment'] = segmapper2.mapped
df2.to_csv('df2_test_data.csv')

