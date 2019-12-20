# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 16:51:58 2019

@author: jankos
"""
from datetime import datetime
import pandas as pd
import numpy as np
from .biman_helpers import str2num, count_activity_change

class NoiseAdder():
    def __init__(self, event_col, target_col, targets, data):
        self.original_data = data
        self.event_col = event_col
        self.target_col = target_col
        self.targets = targets
        self.edited_data = data
        self.stripped = None
    def switch_target(self, p_limit=0.2, length_limit=16):
        if self.stripped is None:
            self.strip_values()

        p = np.random.uniform(0,1,(len(self.stripped),1))
        p_mask = p < p_limit
        len_mask = self.stripped['dif'] < length_limit
        NT_mask = self.stripped[self.target_col] == 'NT'
        T_mask = self.stripped[self.target_col] != 'NT'
#        pdb.set_trace()
        try:
            trues = pd.Series(p_mask.squeeze() & NT_mask.values & len_mask).value_counts().loc[True]
        except KeyError:
            return None
        new_targets = np.random.choice(self.targets, trues)
        self.stripped.loc[p_mask.squeeze() & NT_mask.values & len_mask, self.target_col] = new_targets
        self.stripped.loc[p_mask.squeeze() & T_mask.values & len_mask, self.target_col] = 'NT'
        self.stripped['event:target'] = (self.stripped[self.event_col] +
                                                              ':' + self.stripped[self.target_col])
        self.stripped = self.stripped.rename(columns={'index':'frame'})

    def shift_boundaries(self, shift=4):
        if self.stripped is None:
            self.strip_values()

        if len(self.stripped)>0:
            self.stripped['shifted_frame'] = self.stripped['frame']
            self.stripped.loc[self.stripped['dif'] > 2*shift,'shifted_frame'] = self.stripped.loc[self.stripped['dif']>2*shift,'frame'].apply(lambda x: x + np.random.randint(-shift,shift+1))
            print('shifted')
        return None

    def strip_values(self, event_col, target_col):
        numeral = str2num(self.original_data['event:target'])
        changes, indices = count_activity_change(numeral)
        self.stripped = self.original_data.iloc[indices]
        self.stripped = self.stripped.reset_index(drop=True)
        self.stripped['dif'] = self.stripped['frame'].diff()
        self.stripped = self.stripped.fillna(0)
        self.stripped[self.event_col] = self.stripped['event:target'].apply(lambda x: x.split(':')[0])
        self.stripped[self.event_col] = self.stripped['event:target'].apply(lambda x: x.split(':')[1])

    def get_noisy_df(self):
        """Fill in the frames between annotations, e.g. if frame 10 belongs to event X and frame 25 to event y,
        then frames 10 - 25 are assigned to event x and so on"""
        df_copy = self.stripped.copy()
#        df_copy = df_copy.drop(index=0)
        minimum = df_copy['shifted_frame'].min()
        maximum = df_copy['shifted_frame'].max()
        df_copy = df_copy.drop_duplicates(subset='shifted_frame', keep='last')
        new_index = pd.Index(np.arange(minimum, maximum+1), name='shifted_frame')
        df_copy = df_copy.set_index("shifted_frame").reindex(new_index)

        df_copy = df_copy.reset_index()
        df_copy = df_copy.fillna(method='ffill')

        return df_copy
#
#if __name__ == '__main__':
#        #%%Noisy datasets for validation
#    start_time = datetime.now()
#
#    for (participant, suture), df in dfs_dict.items():
#        print('participant {} suture {}'.format(participant, suture))
#        com = pd.DataFrame()
#        for hand in ['LH', 'RH']:
#            hand_data = df[df['hand'] == hand].reset_index(drop=True)
#            NA = NoiseAdder(hand_data)
#            NA.shift_boundaries(shift=8)
#            NA.switch_target(p_limit=0.8, length_limit=256)
#            noisy = NA.get_noisy_df()
#            com = pd.concat([com, noisy])
#        com = com.reset_index(drop=True)
#
#        com.to_csv('data_out/noise_data/noise_datasets/set8/Noisy_data_8_test_{}_suture_{}.csv'.format(participant, suture))
#
#    print('time to run: {}'.format(datetime.now() - start_time))