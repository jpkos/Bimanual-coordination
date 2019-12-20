# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 21:02:18 2019

@author: jankos
"""
import numpy as np
import pandas as pd
import pdb


def str2num(series):
    """Replace string categorical variables with numerical """
    dictionary = dict(zip(series.unique(), range(len(series))))
    series2 = series.replace(dictionary)
    return series2

def split_hands(data):
    """Take df with data for both hands and return two DFs with hands separated """
    LH = data[data['hand'] == 'LH']
    RH = data[data['hand'] == 'RH']
    LH = LH.reset_index(drop=True)
    RH = RH.reset_index(drop=True)

    return LH,RH


def event_to_numlist(dfcol, taskdict):
    #taskdict = {'grab': 0, 'move':1, 'hold still':2, 'transport':3, 'NV':4}
    num = dfcol.apply(lambda x: taskdict[x])
    numlist = np.int32(np.array(list(num.values)))

    return numlist


def map_segments(frames, segment_borders, segment_names):
    """digitize frame ranges with segment borders, rename with segment names """
    segment_borders[0] = frames.min()
    segment_borders[-1] = frames.max() #just in case annotations for last and first frame didn't match exactly
    bins = np.digitize(frames, segment_borders)
    num_segments = np.unique(bins)
    if len(num_segments) > len(segment_names):
        segment_names = segment_names + [segment_names[-1]]*(len(num_segments)-len(segment_names))
    mapping = dict(zip(np.unique(bins), segment_names))
    named_values = [mapping[value] for value in bins]

    return named_values



def create_value_count_df(values):
    value_counts = values.value_counts()
    value_counts = value_counts.to_frame()
    value_counts = value_counts.reset_index()
    value_counts = value_counts.T
    value_counts.columns = value_counts.iloc[0]
    value_counts = value_counts.reset_index(drop=True)
    value_counts = value_counts.drop(index=0)
    value_counts = value_counts.astype(float)

    return value_counts

def switch_cols(suture_cols, switch_dict):
    cols = suture_cols
    for key, value in switch_dict.items():
        cols[suture_cols.index(key)], cols[value] = suture_cols[value], suture_cols[suture_cols.index(key)]

    return cols

def classification_type(true_col='true_skill', neg_col='novice', pos_col='expert', data=None):
    if data is None:
        print("Data required")
        return None
    positives = data[data[true_col] == pos_col]
    negatives = data[data[true_col] == neg_col]

    TN = negatives[neg_col].sum()
    TE = positives[pos_col].sum()
    FN = positives[neg_col].sum()
    FE = negatives[pos_col].sum()

    return np.array([[TN, FN],[FE, TE]])

def calc_accuracy(cm):
    accuracy = (cm[0][0] + cm[1][1])/cm.sum()
    return accuracy

def drop_duplicate_comparisons(df):
    df['set'] = df.apply(lambda x: {x['p_compared'],
                                    x['p_compared_to'],
                                    x['suture'],
                                    x['segment'],
                                    x['hand']}, axis=1)
    df2=df[~df['set'].astype(str).duplicated(keep='first')]
    return df2.reset_index(drop=True)

