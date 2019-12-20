# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 16:54:43 2019

@author: jankos
"""
#import numpy as np
import pandas as pd
class Participant():
    def __init__(self, ID):
        self.annotations = pd.DataFrame()
        self.Sutures = 0
        self.ID = ID
        self.frames = 0
        self.segments = []

    def set_annotations(self, annotations):
        self.annotations = annotations
        self.annotations = self.annotations[self.annotations['frame'] != 0]
        self.annotations = self.annotations.sort_values(['suture','frame'])

    def get_frame_stamps(self):
        """Get frame stamps, i.e. the frames at which events like 'needle piercing' occurred"""
        framestamps = []
        self.sutures = self.annotations['suture'].unique() #How many & what sutures were done (out of 12)
        #group by 'suture'
        grouped = self.annotations.groupby(by='suture')
        #framenames = grouped.get_group(1)['action'].tolist() #Takes the names of segments from first suture
        for suture in self.sutures:
            framestamps.append(grouped.get_group(suture)['frame'].astype(int).tolist())
        self.frames = framestamps

    def get_segments(self):
        segment_borders = self.annotations['action'].unique()
        segment_borders[segment_borders == 'throw3 end'] = 'cut'
        segment_borders = segment_borders[:-1]
        self.segments = segment_borders

    def find_segment(self, segment_name, suture):
        segment_id = self.segments[segment_name]
        segment_frames = self.frames[suture-1][segment_id:segment_id+2]

        return (segment_frames[0], segment_frames[1])