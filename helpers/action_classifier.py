# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 18:44:56 2019

@author: jankos
"""

import pandas as pd
import numpy as np

class Action_classifier():
    def __equalize_hands(self, LH, RH, frame_col='frame'):
        """Sometimes hands were annotated from slightly different frame range. This
        function makes them equal by shortening the longer one and vice versa"""
        min_RH = RH[frame_col].min()
        min_LH = LH[frame_col].min()
        max_RH = RH[frame_col].max()
        max_LH = LH[frame_col].max()

        RH = RH[RH[frame_col].between(max([min_RH,min_LH]), min([max_LH,max_RH]), inclusive=True)]
        LH = LH[LH[frame_col].between(max([min_RH,min_LH]), min([max_LH,max_RH]), inclusive=True)]

        LH = LH.reset_index(drop=True)
        RH = RH.reset_index(drop=True)
        return LH, RH

    def __classify_action(self, tasks, targets):
        """Classify hands as balanced, master/slave, NTR (non-task related),
        or Single hand movement."""
        LH_task, RH_task = tasks
        LH_target, RH_target = targets
        action_type = ['','']
    #    pdb.set_trace()
        if 'NT' not in targets and 'hold still' not in tasks:
            action_type = ['balanced', 'balanced']
        elif LH_task == 'hold still' and LH_target != 'NT':
            if RH_target != 'NT':
                action_type = ['slave', 'master']
            else:
                action_type = ['Single', 'NTR']
        elif RH_task == 'hold still' and RH_target != 'NT':
            if LH_target != 'NT':
                action_type = ['master', 'slave']
            else:
                action_type = ['NTR', 'Single']
        elif RH_target != 'NT' and LH_target == 'NT':
            action_type = ['NTR', 'Single']
        elif LH_target != 'NT' and RH_target == 'NT':
            action_type = ['Single', 'NTR']
        elif LH_target == 'NT' and RH_target == 'NT':
            action_type = ['NTR', 'NTR']
        else:
            action_type = ['undefined', 'undefined']

        return action_type

    def classify_df_action(self,task_col='event', target_col='target', hand_col='hand', data=None):
        # pdb.set_trace()

        if data is None:
            print('Data required')
            return None
        """Take a dataframe with hand actions and classify the actions"""
        LH, RH = [data.reset_index() for i, data in data.groupby(hand_col)]
        LH, RH = self.__equalize_hands(LH, RH)
        # pdb.set_trace()
        df2 = pd.DataFrame({'LH_task':LH[task_col], 'RH_task':RH[task_col],
                            'LH_target':LH[target_col], 'RH_target':RH[target_col]})

        actions = df2.apply(lambda row: self.__classify_action([row['LH_task'], row['RH_task']],
                                            [row['LH_target'], row['RH_target']]), axis=1)

        actions = pd.DataFrame(item for item in actions)
        actions.columns = ['LH', 'RH']
        return actions