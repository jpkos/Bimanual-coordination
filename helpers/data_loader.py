# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 17:40:08 2019

@author: jankos
"""
import pandas as pd
from .participant import Participant
from config import segments
#%%
#Load annotations and create a list of p objects
def load_participants(participants_list, path, drop_segments):
    ps_dict = {}
    for p in participants_list:
        if p == 'P3' or p == 'p03': #P3's file had to be modified a bit because of failed sutures
            final_path = ('{}/{}annotations_mod2.csv'.format(path, p.upper()))
        else:
            final_path = ('{}/{}annotations.csv'.format(path,p.upper()))
        annotations = pd.read_csv(final_path)
        annotations = annotations[~annotations['action'].isin(drop_segments)]
        # pdb.set_trace()
        part = Participant(p)
        part.set_annotations(annotations)
        part.get_segments()
        part.get_frame_stamps()
        ps_dict[p] = part
    return ps_dict

#%%
#Create a dict of ps and sutures and the corresponding dataframes with annotated data
def load_data(participants_list, sutures_list, path, filename):
    dfs_dict = {}
    for p in participants_list:
        for suture in sutures_list:
            file = filename.format(p, suture)
            final_path = ('{}/{}.csv'.format(path, file))
            data = pd.read_csv(final_path, index_col=[0])
            data.reset_index(drop=True, inplace=True)
            dfs_dict[(p, suture)] = data
    return dfs_dict

#%% Read and save uwomsa b values from Antti's files
#uwo = pd.read_csv(r'C:\Users\jankos\Desktop\Tyokansio\Projektit\Bimanual_coordination\UWOMSA_modified.csv', sep=';')
#k = pd.read_csv(r'C:\Users\jankos\Desktop\Tyokansio\Projektit\Bimanual_coordination\key_index.csv', sep=';')
#ps = ['p02', 'p03', 'p05', 'p06', 'p07', 'p08', 'p09', 'p10', 'p11', 'p12']
#uwb_list = []
#pnew_list = []
#sutures_list = []
#for p in ps:
#    for suture in [1,2,3,4,5]:
#        uwb = hf.get_anttis_ratings(k, uwo, suture, p)
#        uwb_list.append(uwb.iloc[:,1].values[0])
#        pnew_list.append(p)
#        sutures_list.append(suture)
#uwomsas = pd.DataFrame({'p':pnew_list, 'suture':sutures_list,'uwomsa_b': uwb_list})
