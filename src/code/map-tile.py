import cv2
import numpy as np
from skimage.measure import regionprops
import os

class Tile:
    """X-Pos, Y-Pos, Radius, contents"""

    def __init__(self, X_Pos: int, Y_Pos: int, Radius: int, Contents: str = ""):
        self.x = X_Pos
        self.y = Y_Pos
        self.radius = Radius
        self.contents = Contents
        
    def Draw(self):
        Return