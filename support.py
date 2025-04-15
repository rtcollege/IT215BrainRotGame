import os
import pygame

def import_image(path):
    """Import a single image and return the surface"""
    return pygame.image.load(path).convert_alpha()

def import_folder(path):
    """Import all images from a folder"""
    surface_list = []
    
    for image in os.listdir(path):
        full_path = os.path.join(path, image)
        if os.path.isfile(full_path):
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
            
    return surface_list

def import_folder_dict(path):
    """Import images from a folder and return them in a dictionary with filenames as keys"""
    surface_dict = {}
    
    for image in os.listdir(path):
        full_path = os.path.join(path, image)
        if os.path.isfile(full_path):
            image_surf = pygame.image.load(full_path).convert_alpha()
            # Store without file extension
            name = os.path.splitext(image)[0]
            surface_dict[name] = image_surf
            
    return surface_dict

def import_subfolder_dict(root_path):
    """Import images from all subfolders and return nested dictionary"""
    assets_dict = {}
    
    for root, dirs, files in os.walk(root_path):
        if files:
            # Get relative path from root directory
            rel_path = os.path.relpath(root, root_path)
            # Split path into parts for nested dict creation
            path_parts = rel_path.split(os.sep)
            
            # Create nested dictionary structure
            current_dict = assets_dict
            for part in path_parts[:-1]:
                current_dict = current_dict.setdefault(part, {})
            
            # Add images to the deepest level
            folder_name = path_parts[-1] if path_parts[-1] != '.' else 'root'
            current_dict[folder_name] = import_folder_dict(root)
            
    return assets_dict
