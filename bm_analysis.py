# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 15:48:59 2019

@author: jankos
"""
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import helperFunctions as hf
import config as con
import pdb

# import biman_helpers as bm
import helpers as bm


# %% Label segments
def add_segments(dfs_dict, participants_dict):
    for (participant, suture), actions in dfs_dict.items():
        panno = participants_dict[participant]
        frames = panno.frames[suture - 1].copy()
        segment_names = panno.segments
        # pdb.set_trace()
        # print('participant {} suture {}'.format(participant, suture))
        seg_mapper = bm.Segment_mapper(frames, segment_names)
        seg_mapper.remove_doubled()
        seg_mapper.map_segments(actions['frame'])
        # pdb.set_trace()
        actions['segment'] = seg_mapper.mapped
        # pdb.set_trace()


# %%This calculates the ratios of different task:target pairs for different segments
def calc_label_ratios(dfs_dict):
    segment_ratios_df = pd.DataFrame()
    for (participant, suture), actions in dfs_dict.items():
        actions.dropna(inplace=True, subset=['segment'])
        hand_group = actions.groupby(by=['hand', 'segment'])
        # calculate
        activity_counts = hand_group.apply(lambda x: bm.create_value_count_df(x['event:target']))
        activity_counts.fillna(value=0, inplace=True)
        activity_ratios = activity_counts.apply(bm.calc_normalization, axis=1)
        activity_ratios.reset_index(inplace=True)
        activity_ratios['participant'] = [participant] * len(activity_ratios)
        activity_ratios['suture'] = [suture] * len(activity_ratios)
        segment_ratios_df = pd.concat([segment_ratios_df, activity_ratios], sort=True)

    segment_ratios_df.fillna(value=0, inplace=True)
    try:
        segment_ratios_df.drop(columns=['level_2'], inplace=True)
    except KeyError:
        pass
    # Switch column locations
    cols = list(segment_ratios_df.columns)
    switch = {'participant': 0, 'suture': 1, 'segment': 2, 'hand': 3}
    new_cols = bm.switch_cols(suture_cols=cols, switch_dict=switch)
    segment_ratios_df = segment_ratios_df[cols]
    segment_ratios_df.reset_index(drop=True, inplace=True)
    segment_ratios_df.fillna(value=0, inplace=True)

    return segment_ratios_df


##segment_ratios_df.to_csv('{}/noise_set{}_action_ratios.csv'.format(con.noise_output_path,noise_set))
# %% Calculate bimanual and suturing efficiencies
# For sutures
def calc_suture_efficiencies(dfs_dict):
    suture_eff_df = pd.DataFrame()
    for (participant, suture), df in dfs_dict.items():
        df = df.copy()
        print('participant {} suture {}'.format(participant, suture))
        # Classify actions (eg. is it bimanual, single, non-task related)
        actions = df.groupby(['hand'])
        # df2 = df.copy()
        bcs, ms = actions.apply(
            lambda x: bm.bcs_ratio(x['action_class'])[0])  # Bimanual coordination skill same for both hands
        # pdb.set_trace()
        eff = actions.apply(lambda x: bm.surg_efficiency(x['action_class']))
        eff = eff.reset_index()
        eff.rename(columns={0: 'efficiency'}, inplace=True)
        eff['bcs_ratio'] = bcs
        eff['participant'] = [participant] * len(eff)
        eff['suture'] = [suture] * len(eff)
        suture_eff_df = pd.concat([suture_eff_df, eff])

    return suture_eff_df


# %% Add uwomsa scores to same DF as ratios
# uwomsas = pd.read_csv(con.uwomsa_path)
def add_uwomsa_scores(suture_eff_df, uwomsas):
    uwomsas['pnew'] = uwomsas['participant'].apply(lambda x: int(x[1:]))
    uwomsas.sort_values(by=['pnew', 'suture'], inplace=True)
    suture_eff_df['skill'] = suture_eff_df['participant'].map(con.skill_map)
    suture_eff_df['pnew'] = suture_eff_df['participant'].apply(lambda x: int(x[1:]))
    suture_eff_df.sort_values(by=['pnew', 'suture'], inplace=True)
    suture_eff_df.reset_index(drop=True, inplace=True)
    uwomsas.reset_index(drop=True, inplace=True)
    suture_eff_df['uwomsa_b'] = uwomsas['uwomsa_b']


# suture_eff_df.to_csv('{}/noise_set{}_Efficiencies_both_hands.csv'.format(con.noise_output_path,noise_set))
# %%Efficiencies for segments
def calc_segment_efficiencies(dfs_dict, frame_col='frame'):
    seg_eff_df = pd.DataFrame()
    for (participant, suture), df in dfs_dict.items():
        print('{} {}'.format(participant, suture))
        df_grouped = df.groupby(by=['hand', 'segment'])
        bcs = df_grouped.apply(lambda x: bm.bcs_ratio(x['action_class'])[0])
        eff = df_grouped.apply(lambda x: bm.surg_efficiency(x['action_class']))
        eff = eff.reset_index()
        eff.rename(columns={0: 'efficiency'}, inplace=True)
        eff['participant'] = [participant] * len(eff)
        eff['bcs_ratio'] = bcs.values
        eff['suture'] = [suture] * len(eff)
        seg_eff_df = pd.concat([seg_eff_df, eff])

    return seg_eff_df


# %% Fix some missing values and save

def fix_seg_eff(seg_eff_df):
    seg_eff_df2 = seg_eff_df.copy()
    new_row = pd.Series({'participant': 'p10', 'suture': 1, 'segment': 'cut', 'bcs': 0,
                         'LH_efficiency': 0, 'RH_efficiency': 0},
                        name=35)  # participant 10 didn't cut thread ends at suture 5
    seg_eff_df2.sort_index(inplace=True)
    seg_eff_df2 = seg_eff_df2.append(new_row, ignore_index=False)
    seg_eff_df2.loc[237] = ['p3', 5, 'cut', 0, 0, 0]  # same as above
    seg_eff_df2.sort_index(inplace=True)
    seg_eff_df2.reset_index(drop=True, inplace=True)
    seg_eff_df2['skill'] = seg_eff_df2['participant'].map(con.skill_map)


# %%Calculate similarities (better method)
# Previously we compared everyone to average novice and average expert. Now we compare everyone to everyone
def calc_similarities(segment_ratios_df):
    def df_func(row, df, func):
        mask = ((df['participant'] != row['participant']) & (df['suture'] == row['suture']) &
                    (df['segment'] == row['segment']) & (df['hand'] == row['hand']))
        rest = df[mask].select_dtypes(float) #Mistä indeksistä alkaen poistetaan (turhat sarakkeet)?
        # pdb.set_trace()
        row_val = row[row.apply(type) == float]
        # pdb.set_trace()
        results = rest.apply(lambda x: func(x, row_val), axis=1)
        results_df = df[mask][['participant', 'suture', 'segment', 'hand']]
        results_df['similarity'] = results
        results_df['p_compared'] = row['participant']
        results_df = results_df.rename(columns={'participant': 'p_compared_to'})
        return results_df

    ad = segment_ratios_df.apply(lambda x: df_func(x, segment_ratios_df, bm.distance_projection), axis=1,
                                 result_type='reduce')
    sim2_df = pd.concat(ad.values.tolist())
    sim2_df.reset_index(drop=True)
    sim2_df = bm.drop_duplicate_comparisons(sim2_df)
    return sim2_df


# %% classification by comparing how many sutures were closer to expert vs.
# how many were closer to novice
# Group by participant who was compared, suture, hand, skill to which the participant was compared
def sim_suture_reshape(sim_df):
    sim2_df = sim_df.copy()
    sim_grouped = sim2_df.groupby(['p_compared', 'suture', 'hand', 'skill_compared_to']).mean()
    sim_grouped.reset_index(inplace=True)
    sim_grouped.rename(columns={'similarity': 'average_similarity'}, inplace=True)
    # Groupby skill of comparison target
    sim_skill = list(sim_grouped.groupby('skill_compared_to'))
    # 1st experts
    skill_reshaped = sim_skill[0][1].rename(columns={'average_similarity': 'expert_similarity'})
    skill_reshaped.reset_index(drop=True, inplace=True)
    # Then novices, combine these to same df
    skill_reshaped['novice_similarity'] = sim_skill[1][1]['average_similarity'].reset_index(drop=True)
    # Is the participant closer to experts?
    skill_reshaped['expert'] = skill_reshaped['expert_similarity'] > skill_reshaped['novice_similarity']
    skill_reshaped['skill'] = skill_reshaped['p_compared'].map(con.skill_map)
    return skill_reshaped.reset_index(drop=True)


# %%
def sim_suture_classification(skill_reshaped):
    skill_counts = skill_reshaped.groupby(['p_compared', 'hand', 'expert']).size().unstack(fill_value=0)
    skill_counts.columns = ['novice', 'expert']
    skill_counts.reset_index(drop=False, inplace=True)
    skill_counts['classification'] = skill_counts.apply(lambda x: 'expert' if x['expert'] > x['novice'] else 'novice',
                                                        axis=1)
    skill_counts['true_skill'] = skill_counts['p_compared'].map(con.skill_map)
    skill_counts['correct_prediction'] = skill_counts['true_skill'] == skill_counts['classification']
    return skill_counts


# %% Classification at segment level (averaged segments)
def sim_avsegment_classification(sim_df):
    sim2_df = sim_df.copy()
    av_segmentsim = sim2_df.groupby(['p_compared', 'segment', 'hand', 'skill_compared_to']).mean()
    av_segmentsim.reset_index(drop=False, inplace=True)
    av_segmentsim['skill'] = av_segmentsim['p_compared'].map(con.skill_map)
    # Split by the skill of the comparison target into two columns
    av_segmentsim_ex = av_segmentsim[av_segmentsim['skill_compared_to'] == 'expert']
    av_segmentsim_ex.rename(columns={'similarity': 'ex_similarity'}, inplace=True)
    av_segmentsim_no = av_segmentsim[av_segmentsim['skill_compared_to'] == 'novice']
    av_segmentsim_ex.reset_index(drop=True, inplace=True)
    av_segmentsim_no.reset_index(drop=True, inplace=True)
    # Combine the dfs again to one with the original columns in two columns
    av_segmentsim2 = av_segmentsim_ex.copy()
    av_segmentsim2['no_similarity'] = av_segmentsim_no['similarity']
    av_segmentsim2.drop(columns=['skill_compared_to', 'suture'], inplace=True)
    av_segmentsim2['predicted_skill'] = av_segmentsim2.apply(
        lambda x: 'expert' if x['ex_similarity'] > x['no_similarity'] else 'novice', axis=1)
    # Correct prediction = How many correctly predicted segments?
    av_segmentsim2['correct_prediction'] = av_segmentsim2['skill'] == av_segmentsim2['predicted_skill']
    av_segmentsim2['correct_prediction'] = av_segmentsim2['correct_prediction'].astype(int)
    summed = av_segmentsim2.groupby(['p_compared', 'hand']).sum()
    summed.reset_index(inplace=True)

    return summed


# %%Classification at segment level (non-averaged segments)
def sim_segment_classification(sim_df):
    sim2_df = sim_df.copy()
    segmentsim = sim2_df.groupby(['p_compared', 'segment', 'hand', 'skill_compared_to', 'suture']).mean()
    segmentsim.reset_index(inplace=True)
    # Split combine, like above
    segmentsim_ex = segmentsim[segmentsim['skill_compared_to'] == 'expert']
    segmentsim_no = segmentsim[segmentsim['skill_compared_to'] == 'novice']
    segmentsim_ex.sort_values(by=['p_compared', 'suture', 'segment', 'hand'], inplace=True)
    segmentsim_no.sort_values(by=['p_compared', 'suture', 'segment', 'hand'], inplace=True)
    segmentsim_ex.reset_index(drop=True, inplace=True)
    segmentsim_no.reset_index(drop=True, inplace=True)
    segmentsim = segmentsim_ex.copy()
    segmentsim.rename(columns={'similarity': 'ex_similarity'}, inplace=True)
    segmentsim['no_similarity'] = segmentsim_no['similarity']
    segmentsim.drop(columns=['skill_compared_to'], inplace=True)
    # Predict, like above
    segmentsim['predicted_skill'] = segmentsim.apply(
        lambda x: 'expert' if x['ex_similarity'] > x['no_similarity'] else 'novice', axis=1)
    # Correct prediction = How many correctly predicted segments?
    segmentsim['skill'] = segmentsim['p_compared'].map(con.skill_map)
    segmentsim['correct_prediction'] = segmentsim['skill'] == segmentsim['predicted_skill']
    segmentsim['correct_prediction'] = segmentsim['correct_prediction'].astype(int)
    summed = segmentsim.groupby(['p_compared', 'hand', 'segment']).sum()
    summed.drop(columns=['ex_similarity', 'no_similarity', 'suture'], inplace=True)
    summed.reset_index(inplace=True)

    return summed

# %%
