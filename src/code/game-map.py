"""Game Map Class
This handles the texture_file, , grid pentagon containing unit,
can render the map,
map supports Z layer maps also"""

import os
import logging
import json
import cv2
import numpy as np
from skimage.measure import regionprops

class GameMap:
    """ Storage Array """

    def __ini__(self,texture_file_path: str,layout_file_path: str, UnitGrid: list =  [[]]):
        
        self.texture_file_path = texture_file_path
        self.layout_file_path = layout_file_path
        self.UnitGrid = UnitGrid
        self.zLayers = 1
        self.Tiles = dict()

        # Load layout file
        self.load_map_layout()

        # Load map tiles
        self.load_map_Tiles()

        #
        
    def to_dict(self):
        return {
            'texture_file_path' :   self.texture_file_path,
            'layout_file_path' :    self.layout_file_path,
            'UnitGrid'  :   self.UnitGrid,
            'zLayers' : self.zLayers,
            'Tiles': self.Tiles
        }
    
    def MapSize(self):
         """ Function to return the total count of tiles """
         return len(self.Tiles)


    def load_map_layout(self):
         """
        Reads a local JSON file and returns the data as a Python object.

        Args:
            file_path (str): The path to the JSON file.

        Returns:
            dict or list: The JSON data as a Python dictionary or list, or None if an error occurs.
        """
        try:
            with open(self.layout_file_path, 'r') as file:
                self.Tiles = json.load(file)
        except FileNotFoundError:
            print(f"Error: File not found at {self.layout_file_path}")
            return None
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in {self.layout_file_path}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None


    def process_jpeg_hexagons(image_path, hexagon_size=20):
            """
            Loads a JPEG image, breaks it into hexagons, and processes them.

            Args:
                image_path (str): Path to the JPEG image.
                hexagon_size (int): Size of the hexagons (approximate radius).

            Returns:
                list: A list of hexagon data (e.g., center coordinates, average color).
            """

            img = cv2.imread(image_path)
            if img is None:
                raise FileNotFoundError(f"Could not open or find the image: {image_path}")

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            height, width = gray.shape

            hexagon_data = []

            for y in range(0, height, int(hexagon_size * 1.5)): # Adjust step for hexagonal grid
                for x_offset, x in enumerate(range(0, width, int(hexagon_size * 1.732))): # Adjust step for hexagonal grid
                    x_adjusted = x + (hexagon_size * 0.866 if y % (int(hexagon_size*1.5)) != 0 else 0) # Adjust x based on row.
                    x_int = int(x_adjusted)
                    y_int = int(y)

                    # Create a hexagonal mask
                    mask = np.zeros_like(gray, dtype=np.uint8)
                    points = []
                    for i in range(6):
                        angle_deg = 60 * i - 30
                        angle_rad = np.pi / 180 * angle_deg
                        px = int(x_int + hexagon_size * np.cos(angle_rad))
                        py = int(y_int + hexagon_size * np.sin(angle_rad))
                        points.append([px, py])
                    points = np.array(points, np.int32)
                    cv2.fillPoly(mask, [points], 255)

                    # Extract the hexagon region
                    hexagon_region = cv2.bitwise_and(img, img, mask=mask)

                    # Check if all pixels are black
                    gray_hexagon = cv2.cvtColor(hexagon_region, cv2.COLOR_BGR2GRAY)
                    if np.all(gray_hexagon == 0):
                        continue  # Skip all-black hexagons

                    # Calculate average color (or other properties)
                    mean_color = cv2.mean(hexagon_region, mask=mask)[:3] #B,G,R

                    # Calculate the region properties
                    props = regionprops(mask)
                    center_y, center_x = props[0].centroid

                    hexagon_data.append({
                        "center": (center_x, center_y),
                        "mean_color": mean_color,
                    })

            return hexagon_data