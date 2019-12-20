# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 18:46:54 2019

@author: jankos
"""
import numpy as np
import pandas as pd

class Segment_mapper():
    def __init__(self, frames, segment_names):
        self.frames = frames
        self.segment_names = segment_names
        self.mapped = None

    def remove_doubled(self):
        doubled = np.array(np.argwhere(np.diff(self.frames) == 0))
        self.segment_names = np.delete(np.array(self.segment_names), doubled-1)
        self.frames = np.delete(np.array(self.frames), doubled)


    def map_segments(self, actions):
        self.mapped = pd.cut(actions, self.frames, labels=self.segment_names,
                             duplicates='drop')