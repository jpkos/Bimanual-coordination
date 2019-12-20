# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 15:15:15 2019

@author: jankos
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
# import .biman_helpers as bm
sns.set(font_scale=2)
#%%Load data
similarities = pd.read_csv(r"C:\Users\jankos\Desktop\Tyokansio\Projektit\Bimanual_coordination\biman\src\suture_similarity_testnew.csv")
#%%
a=seg_df2
segments = ['needle pick', 'piercing', 'thread handling', 'knot1', 'knot2', 'knot3', 'cut']
segments_ordered = dict(zip(segments, [x for x in range(len(segments))]))
a['seg_ord'] = a['segment'].map(segments_ordered)
a.sort_values(by=['participant', 'suture', 'seg_ord'],inplace=True)
#%% Plot all
#Scatterplot for similarity
fig, ax = plt.subplots(figsize=(15,7),nrows=1,ncols=2)
#sns.scatterplot(x='LH_ex', y='LH_no', hue='skill', data=sim_group,s=200,palette='cubehelix', ax=ax[0])
#sns.scatterplot(x='RH_ex', y='RH_no', hue='skill', data=sim_group,s=200,palette='cubehelix',ax=ax[1])
sns.scatterplot(x='expert_similarity',y='novice_similarity', hue='skill',
                data=similarities[similarities['hand'] == 'LH'],s=200,palette='cubehelix', ax=ax[0])
sns.scatterplot(x='expert_similarity',y='novice_similarity', hue='skill',
                data=similarities[similarities['hand'] == 'RH'],s=200,palette='cubehelix',ax=ax[1])

handles, labels = ax[1].get_legend_handles_labels()
ax[0].get_legend().remove()
ax[1].get_legend().remove()
ax[0].set(xlabel='', ylabel='Similarity to novice', xlim=(0,1), ylim=(0,1), title='NDH')
ax[1].set(xlabel='', ylabel='', xlim=(0.0,1.0), ylim=(0,1), title='DH')
fig.legend(handles, labels, loc='upper right', markerscale=4)
fig.text(0.45, 0.015,'Similarity to expert')
plt.tight_layout()
plt.show()
#%%Boxplot for suturing efficiency
#%%ratios
fig, ax = plt.subplots(figsize=(15,7),nrows=1,ncols=2,sharey=True)
sns.boxplot(x='skill', y='LH_efficiency', data=ratio_df, linewidth=2, ax=ax[0], palette='cubehelix')
sns.boxplot(x='skill', y='RH_efficiency', data=ratio_df, linewidth=2, ax=ax[1], palette='cubehelix')
#ax[0].get_legend().remove()
#ax[1].get_legend().remove()
ax[0].set(xlabel='', ylabel='Efficiency', title='NDH')
ax[1].set(xlabel='', ylabel='', title='DH')
#fig.legend(handles, labels, loc='upper right')
fig.text(0.5, 0.015,'Skill')
plt.tight_layout()
plt.show()
#%%Boxplot for bimanual efficiency
fig, ax = plt.subplots(figsize=(8,7),nrows=1,ncols=1,sharey=True)
sns.boxplot(x='skill', y='bcs_ratio', data=ratio_df, linewidth=2, ax=ax, palette='cubehelix')
#sns.boxplot(x='skill', y='bcs_ratio', data=RHratios, linewidth=2, ax=ax[1], palette='cubehelix')
#ax[0].get_legend().remove()
#ax[1].get_legend().remove()
ax.set(xlabel='skill', ylabel='Bimanual dexterity')
#ax[1].set(xlabel='', ylabel='', title='Right hand')
#fig.legend(handles, labels, loc='upper right')
#fig.text(0.5, 0.015,'Skill')
plt.tight_layout()
plt.show()
#%%UWOMSA Scatter
ratios = ratio_df.copy()

fig, ax = plt.subplots(figsize=(15,7),nrows=1,ncols=2,sharey=True)
sns.scatterplot(x='LH_efficiency', y='uwomsa_b', hue='skill', data=ratio_df, s=200, ax=ax[0], palette='cubehelix')
sns.scatterplot(x='RH_efficiency', y='uwomsa_b', hue='skill', data=ratio_df, s=200, ax=ax[1], palette='cubehelix')
handles, labels = ax[1].get_legend_handles_labels()
ax[0].get_legend().remove()
ax[1].get_legend().remove()
ax[0].set(xlabel='', ylabel='UWOMSA B', title='NDH', xlim=(0.2,1))
ax[1].set(xlabel='', ylabel='', title='DH', xlim=(0.2,1))
fig.legend(handles, labels, loc='best', bbox_to_anchor=(0.50,0.1,0.5,0.5))
fig.text(0.43, 0.015,'Suturing efficiency')
#plt.tight_layout()
plt.show()

#%% Segment-wise similarities
a = pd.read_csv(r'C:\Users\jankos\Desktop\Tyokansio'
                r'\Projektit\Bimanual_coordination\output_data'
                r'\similarities_by_segments.csv', index_col=[0])

exp_a = a[a['skill'] == 'expert']
nov_a = a[a['skill'] == 'novice']
#%%
plt.close()
fig, ax = plt.subplots(figsize=(14,12), nrows=2, ncols=2, sharex=True, sharey=True)
sns.catplot(x='segment', y='no_similarity', kind='point', hue='skill', palette='cubehelix', data=segmentsim[segmentsim['hand'] == 'LH'], ax=ax[0,0])
sns.catplot(x='segment', y='ex_similarity', kind='point', hue='skill', palette='cubehelix', data=segmentsim[segmentsim['hand'] == 'LH'], ax=ax[1,0])
sns.catplot(x='segment', y='no_similarity', kind='point', hue='skill', palette='cubehelix', data=segmentsim[segmentsim['hand'] == 'RH'], ax=ax[0,1])
sns.catplot(x='segment', y='ex_similarity', kind='point', hue='skill', palette='cubehelix', data=segmentsim[segmentsim['hand'] == 'RH'], ax=ax[1,1])
ax[1,1].tick_params(labelrotation=65)
ax[1,0].tick_params(labelrotation=65)
ax[1,0].set(xlabel='', ylim=(0,1), ylabel='NDH similarity expert')
ax[0,0].set(xlabel='', ylabel='NDH similarity novice')
ax[0,1].set(xlabel='', ylabel='DH similarty novice')
ax[1,1].set(xlabel='', ylabel='DH similarity expert')
handles, labels = ax[0,0].get_legend_handles_labels()
ax[0,0].get_legend().remove()
ax[0,1].get_legend().remove()
ax[1,0].get_legend().remove()
ax[1,1].get_legend().remove()
fig.legend(handles, labels, loc='center', bbox_to_anchor=(0.67,0.5,0.5,0.5), markerscale=4)
#plt.tight_layout()
fig.subplots_adjust(right=0.85)
plt.show()
for p in [2,3,4,5]:
    plt.close(p)

#%%Segment-wise efficiencies
segments = ['needle pick', 'piercing', 'thread handling', 'knot1', 'knot2', 'knot3', 'cut']
segments_ordered = dict(zip(segments, [x for x in range(len(segments))]))
seg_df2['segment_ord'] = seg_df2['segment'].map(segments_ordered)
seg_df2 = seg_df2.sort_values(by=['participant', 'suture', 'segment_ord'])
seg_df2 = seg_df2.reset_index(drop=True)
seg_df3 = seg_df2.copy()
seg_df2 = seg_df2.dropna()
seg_df2[['LH_efficiency', 'RH_efficiency']] = seg_df2[['LH_efficiency', 'RH_efficiency']].astype(float)
#%%
fig, ax = plt.subplots(figsize=(14,7), nrows=1, ncols=2)
sns.catplot(x='segment', y='LH_efficiency', kind='point',
            palette='cubehelix', hue='skill', data=seg_df2, ax=ax[0])
sns.catplot(x='segment', y='RH_efficiency', kind='point',
            palette='cubehelix', hue='skill', data=seg_df2, ax=ax[1])
handles, labels = ax[1].get_legend_handles_labels()
ax[1].tick_params(labelrotation=65)
ax[0].tick_params(labelrotation=65)
ax[0].get_legend().remove()
ax[1].get_legend().remove()
ax[0].set(xlabel='', ylabel='Efficiency', title='Left hand')
ax[1].set(xlabel='', ylabel='', title='Right hand')
fig.legend(handles, labels, loc='best', bbox_to_anchor=(0.51,0.1,0.5,0.5))

plt.show()
#%% Segment-wise bimanual dexterity
fig, ax = plt.subplots(figsize=(12,12))
sns.catplot(x='segment', y='bcs', kind='point',
            palette='cubehelix', hue='skill', data=a, ax=ax)
ax.tick_params(labelrotation=65)
handles, labels = ax.get_legend_handles_labels()
ax.get_legend().remove()
fig.legend(handles, labels, loc='best', bbox_to_anchor=(0.50,0.1,0.5,0.5), markerscale=4)
plt.show()