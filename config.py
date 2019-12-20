# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 16:49:21 2019

@author: jankos
"""
#%%

participants = ['p11', 'p10', 'p9', 'p8', 'p12', 'p2', 'p3', 'p6', 'p7','p5']
segments = ['needle pick', 'piercing', 'thread handling', 'knot1', 'knot2', 'knot3', 'cut']
hands = ['LH', 'RH']
skill_map = {'P2':'novice', 'P3':'novice', 'P5':'expert', 'P6':'expert', 'P7':'expert',
             'P8':'novice', 'P9':'expert', 'P10':'novice', 'P11':'novice', 'P12':'expert'}
#%% paths
segment_annotations_path = ('C:/Users/jankos/Desktop/Tyokansio/scripts2/dataa')

hand_path = (r'C:/Users/jankos/Dropbox/Tyoprojektit'
            r'/Edmonton 2019 Bimanual analysis'
            r'/output_data')

actual_data_path = ('C:/Users/jankos/Desktop/Tyokansio/Projektit/Bimanual_coordination/biman/data/data_in')
noise_data_path = (r'C:/Users/jankos/Desktop/Tyokansio/Projektit/Bimanual_coordination'
             r'/biman/data/data_out/noise_data/noise_datasets')
test_data_path = (r'C:\Users\jankos\Desktop\Tyokansio\Projektit\Bimanual_coordination\biman\src\test')

segment_ratios_savepath = ('data_out/action_ratios/')
suture_eff_savepath = ('data_out/suturing_efficiency/')

uwomsa_path = (r'C:/Users/jankos/Desktop/Tyokansio/Projektit/Bimanual_coordination/Uwomsa_b_list.csv')

action_ratios_savepath=(r'C:/Users/jankos/Desktop/Tyokansio/Projektit/Bimanual_coordination'
     r'/biman/data_out/action_ratios/')
noise_output_path = ('C:/Users/jankos/Desktop/Tyokansio/Projektit/Bimanual_coordination/biman/data/data_out/noise_data/noise_output')

