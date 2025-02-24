import numpy as np
import json
import pandas as pd
import networkx as nx
import random
import matplotlib.pyplot as plt
import numpy as np
import math
import pickle
import json

import numpy as np
from stl import mesh
from shapely.geometry import Polygon
from shapely.ops import unary_union

# Function to convert 2D polygon to 3D mesh by adding thickness
def polygon_to_3d_mesh(polygon, thickness=1.0):
    # Get the exterior coordinates of the 2D polygon
    exterior_coords = list(polygon.exterior.coords)
    
    # Create vertices for the top and bottom of the 3D shape
    top_vertices = [(x, y, thickness) for x, y in exterior_coords]
    bottom_vertices = [(x, y, 0) for x, y in exterior_coords]
    
    # Vertices array: two sets of vertices (top and bottom)
    vertices = np.array(top_vertices + bottom_vertices)
    n = len(exterior_coords)
    
    # Create faces (triangles) connecting the top and bottom surfaces
    faces = []
    
    # Create side walls
    for i in range(n):
        next_i = (i + 1) % n
        faces.append([i, next_i, n + next_i])   # Top to bottom
        faces.append([i, n + next_i, n + i])    # Bottom to top
    
    # Create top and bottom surfaces
    for i in range(1, n - 1):
        faces.append([0, i+1, i ])            # Top face
        faces.append([n, n + i, n + i+1])     # Bottom face

    # Convert faces to NumPy array
    faces = np.array(faces)
    
    # Create mesh object
    polygon_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    
    for i, face in enumerate(faces):
        for j in range(3):
            polygon_mesh.vectors[i][j] = vertices[face[j], :]
    
    return polygon_mesh

def merge_3d_meshes(mesh_list):
    # List to hold the vertices and faces of the merged mesh
    vertices = []
    faces = []
    
    # Variable to track the current offset for the face indices
    vertex_offset = 0
    
    # Iterate over each mesh and extract its vertices and faces
    for m in mesh_list:
        # Extract the vertices and faces of the current mesh
        current_vertices = m.vectors.reshape(-1, 3)  # Each face is a set of 3 vertices
        current_faces = np.arange(len(current_vertices)).reshape(-1, 3)
        
        # Append the vertices, and adjust the face indices by the current offset
        vertices.append(current_vertices)
        faces.append(current_faces + vertex_offset)
        
        # Update the vertex offset for the next mesh
        vertex_offset += len(current_vertices)
    
    # Concatenate all the vertices and faces into a single array
    vertices = np.vstack(vertices)
    faces = np.vstack(faces)
    
    # Create a new merged mesh
    merged_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    
    # Fill the new mesh with the vertices and faces
    for i, face in enumerate(faces):
        for j in range(3):
            merged_mesh.vectors[i][j] = vertices[face[j], :]
    
    return merged_mesh

def save_to_stl(seg_thick_dict, thickness, name, frame_thickness = None):
    mesh_list = []
    for k,v in seg_thick_dict.items():
        p = [] 
        for j in v.vertices:
            try: 
                p.append((float(j[0]), float(j[1])))
            except:
                None
        
        mesh_list.append(polygon_to_3d_mesh(Polygon(p), thickness=thickness))
    
    if frame_thickness != None:
        t = frame_thickness
        bottom = Polygon([ (0,0-t), (0,0),(1,0),(1,0-t)])
        top = Polygon([(0,1),(0,1+t), (1,1+t), (1,1)])
        right = Polygon([(1,0-t), (1,1+t), (1+t,1+t), (1+t,0-t)])
        left = Polygon([(0-t,0-t),(0-t,1+t), (0,1+t), (0,0-t)])

        f = [bottom,top,  right, left]

        for f_ in f:            
            mesh_list.append(polygon_to_3d_mesh(f_, thickness=thickness))

    merged_mesh = merge_3d_meshes(mesh_list)

    # Save the merged mesh as an STL file   
    merged_mesh.save(name)

def save_to_json(data_dict, file_path):
    data_dict['segments_dict'] = {key: pol.to_dict() for key, pol in data_dict['segments_dict'].items()}
    data_dict['segment_thickness_dict'] = {key: pol.to_dict() for key, pol in data_dict['segment_thickness_dict'].items()}

    with open(file_path, 'w') as json_file:
        json.dump(data_dict, json_file)

def load_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data