# -*- coding: utf-8 -*-
"""Settings Class.
This handles the saving, and loading of settings for the game
Currently save to local file
"""

import os
import json
import logging

class SettingsSet:
    """ Array used to hold all the settings, using class to have some built in functions and values"""
   
    def __init__(self,Resolution = (1280,1024),FPS = 60,GameTitle = "War Games",FilePath = "./settings.json",Difficulty = 5):

        self.Resolution = Resolution
        self.FPS = FPS
        self.GameTitle = GameTitle
        self.FilePath = FilePath
        self.Difficulty = Difficulty

    def to_dict(self):
        return {
            'Resolution': self.Resolution, 
            'FPS': self.FPS, 
            'GameTitle': self.GameTitle,
            'FilePath' : self.FilePath,
            'Difficulty' : self.Difficulty
            }

    def Save(self, file_path : str = None):
        """
        Write to local file system saving locally
        Using JSON file settings, can be over-ridden for custom save location
        """

        if not file_path:
            file_path = self.FilePath

        try:
            with open(file_path, 'w') as f:
                json.dump([ self.to_dict() for obj in self], f)
        except ValueError as e:
            logging.error(f"Unable to load file: {self.FilePath}")
            logging.error(e)
    
    def Load(self, file_path : str = None):
        """
        Load from file system
        Using JSON file settings, can be over-ridden for custom load location
        """

        if not file_path:
            file_path = self.FilePath

        with open(file_path, 'r') as f:
            data = json.load(f)
            self.Resolution = data['Resolution']
            self.FPS = data['FPS']
            self.GameTitle = data['GameTitle']
            self.FilePath = data['FilePath']
            self.Difficulty = data['Difficulty']
            
