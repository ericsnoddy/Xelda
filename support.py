import pygame
from csv import reader
from os import path, walk

# Information about the game graphics is stored per tile, per row, in corresponding csv files.
# Different string integers represent different entitites, eg '-1' is no entity, '395' is a shoreline obstacle
# Created with Tiled level editor
def import_csv_layout(csv_file_path):
    # Creates a list to store our values; retrieves and appends the values
    terrain_map = []

    with open(csv_file_path) as layout_csv:
        layout = reader(layout_csv, delimiter = ",")
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map

# Import images each as a surface, export the list
def import_folder(folder_path):
    surface_list = []

    # [0] is the path and [1] is the subfolders list; iterate with underscores cause we only want img_files
    for _, __, img_files in walk(folder_path):
        for image in img_files:
            image_surface = pygame.image.load(path.join(folder_path, image)).convert_alpha()
            surface_list.append(image_surface)
    
    return surface_list