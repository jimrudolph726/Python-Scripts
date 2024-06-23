import os
import pandas as pd
import pygame

def import_csv_layout(path):
    if os.path.getsize(path) == 0:
        return []
    df = pd.read_csv(path, header=None, dtype=str)  # Ensure all data is read as strings
    list = df.fillna('').values.tolist()  # Replace NaN with empty string
    return list

def import_graphics(path):
    images = []
    image_files = os.listdir(path)
    for image in image_files:
        full_path = os.path.join(path,image)
        full_path = full_path.replace("\\", "/")
        image = pygame.image.load(full_path).convert_alpha()
        images.append(image)
    return images
        
    
