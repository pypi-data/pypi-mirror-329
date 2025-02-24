import matplotlib.pyplot as plt
import numpy as np
import math
import random
import os
import sys
import networkx as nx

from .Classes import LineSegment

def minDistance_line_point(A, B, E):
    # vector AB
    AB = np.array(B) - np.array(A)
    EB = np.array(B) - np.array(E)
    AE = np.array(E) - np.array(A)
  
    # Calculating the dot product
    AB_BE = np.dot(AB, EB)
    AB_AE = np.dot(AB, AE)
     
    # Case 1
    if (AB_BE > 0):
        # Finding the magnitude
        y = E[1] - B[1]
        x = E[0] - B[0]
        reqAns = np.sqrt(x * x + y * y)

    # Case 2
    elif (AB_AE < 0):
        y = E[1] - A[1]
        x = E[0] - A[0]
        reqAns = np.sqrt(x * x + y * y)
 
    # Case 3
    else:
        reqAns = np.linalg.outer(AB, AE) / np.linalg.norm(AB)
     
    return reqAns

def doLinesIntersect(line1, line2):
    """
    Check if two lines intersect and return the intersection point.

    Args:
    - line1 (Line): The first line segment.
    - line2 (Line): The second line segment.

    Returns:
    - intersect (bool): True if the lines intersect, False otherwise.
    - intersection_point (tuple or None): The intersection point (x, y) if lines intersect, None otherwise.
    """
    
    x1, y1 = line1[0]
    v1, w1 = (np.cos(line1[1]), np.sin(line1[1]))

    x2, y2 = line2[0]
    v2, w2 = (np.cos(line2[1]), np.sin(line2[1]))

    determinant = v1 * w2 - v2 * w1

    if determinant == 0:
        return False, (None, None)

    t1 = ((x2 - x1) * w2 - (y2 - y1) * v2) / determinant
    t2 = ((x2 - x1) * w1 - (y2 - y1) * v1) / determinant

    intersect_x = x1 + v1 * t1
    intersect_y = y2 + w2 * t2

    if -1e-6 < intersect_x < 1 + 1e-6 and -1e-6 < intersect_y < 1 + 1e-6:
        return True, (intersect_x, intersect_y)
    else:
        return False, (None, None)

def seeds(number_of_lines, radius = 0.015, number_of_trials = 10000):
    Line = {}
    line_id = 0
    
    nucleation_points = [(0,0), (1,0), (1,1), (0,1)]
    angle = [0,np.pi/2, np.pi, 3*np.pi/2]
    
    Line = {'b1':[ (0,0), 0], 'b2':[ (1,0), np.pi/2], 'b3':[ (1,1), np.pi], 'b4':[ (0,1), 3*np.pi/2] }
    
    for i in range(number_of_lines):
        new_points =  (random.uniform(0,1), random.uniform(0,1))
    
        line_new_point = []
        for j in range(len(nucleation_points)):
            start = (np.cos(angle[i])*10+nucleation_points[i][0], np.sin(angle[i])*10+nucleation_points[i][1])
            end = (-np.cos(angle[i])*10+nucleation_points[i][0], -np.sin(angle[i])*10+nucleation_points[i][1])
            line_new_point += [minDistance_line_point(start, end, new_points)]
            
        trial = 0
        while  sum(np.array(line_new_point) < radius) != 0 or np.sum( np.sqrt(np.sum((np.array(nucleation_points) - np.array(new_points))**2, axis = 1)) < radius) != 0:
            new_points =  (random.uniform(0,1), random.uniform(0,1))
    
            line_new_point = []
            for j in range(len(nucleation_points)):
                start = (np.cos(angle[i])*10+nucleation_points[i][0], np.sin(angle[i])*10+nucleation_points[i][1])
                end = (-np.cos(angle[i])*10+nucleation_points[i][0], -np.sin(angle[i])*10+nucleation_points[i][1])
                line_new_point += [minDistance_line_point(start, end, new_points)]
            
            trial += 1
    
            if trial > number_of_trials:
                break
    
        if trial <= number_of_trials:
            nucleation_points += [new_points]
            angles = [0, np.pi/4, np.pi/2, 3*np.pi/4]
            angle_new = random.uniform(0, 2*np.pi) #random.choice(angles)#np.pi #random.uniform(0, 2*np.pi)
            angle += [angle_new]
            Line[line_id] = [ new_points ,angle_new]
            line_id += 1
        else:
            print('jammed')
            break
    
    #number of Line
    print("Number of line: ", len(Line))

    return(Line)

def all_intersection(Line):
    intersections_dict = {}

    for k,v in Line.items():
        #intersections_dict[k] = {}
        intersections_dict[k] = {'back':{}, 'front':{}}
    
        for kk,vv in Line.items():
            intersect, (intersect_x, intersect_y) = doLinesIntersect(v ,vv)

            if intersect:
                segment_length = np.sqrt( (v[0][0] - intersect_x)**2 + (v[0][1] - intersect_y)**2)
            
                if intersect_x < v[0][0]:
                    intersections_dict[k]['back'][kk] =  [(intersect_x, intersect_y), segment_length] 
                else:
                    if intersect_x == v[0][0] and intersect_y < v[0][1]:
                        intersections_dict[k]['back'][kk] =  [(intersect_x, intersect_y), segment_length] 
                    else:
                        intersections_dict[k]['front'][kk] =  [(intersect_x, intersect_y), segment_length] 
        intersections_dict[k]['back'] = dict(sorted(intersections_dict[k]['back'].items(), key=lambda e:e[1], reverse = True))
        intersections_dict[k]['front'] = dict(sorted(intersections_dict[k]['front'].items(), key=lambda e:e[1]))

    return intersections_dict

def transform_to_standard_lines(segments):
    
    data = []
    for s in segments:
        start = (s[3], s[4])
        end = (s[5], s[6])
        line = LineSegment(start=start, end=end, id=s[0], neighbors_initial=[s[1], s[2]], neighbors=None)
        data.append(line)
        
    return data

def static_line_graph_generation(Line, intersections_dict):
    borders = ['b1', 'b2', 'b3', 'b4']
    segments = []
    edges = []
            
    for k,v in Line.items():
        if k not in borders:
            #front
            for kk_f, vv_f in intersections_dict[k]['front'].items():
                try:
                    d_k_kk = intersections_dict[kk_f]['back'][k][1]
                    front_coordinate = intersections_dict[kk_f]['back'][k][0]
                    front_id = kk_f
                    where = 'back'
                except:
                    d_k_kk = intersections_dict[kk_f]['front'][k][1]
                    front_coordinate = intersections_dict[kk_f]['front'][k][0]
                    front_id = kk_f
                    where = 'front'
    
                if vv_f[1] > d_k_kk:
                    #check kk neighbors 
                    boolean = []
                    for kkk, vvv in intersections_dict[kk_f][where].items():
                        if vvv[1] < d_k_kk:
                            try:
                                d_kk_kkk = intersections_dict[kkk]['back'][kk_f][1]
                            except:
                                d_kk_kkk = intersections_dict[kkk]['front'][kk_f][1]
    
                            if d_kk_kkk > vvv[1]:
                                boolean += [0]
                            else:
                                boolean += [1]
    
                    #print(k,kk, boolean)
                     
                    if sum(boolean) == 0:
                        #print(k, kk, front_coordinate)
                        break
                        
            #back
            for kk_b, vv_b in intersections_dict[k]['back'].items():
                try:
                    d_k_kk = intersections_dict[kk_b]['back'][k][1]
                    back_coordinate = intersections_dict[kk_b]['back'][k][0]
                    back_id = kk_b
                    where = 'back'
                except:
                    d_k_kk = intersections_dict[kk_b]['front'][k][1]
                    back_coordinate = intersections_dict[kk_b]['front'][k][0]
                    back_id = kk_b
                    where = 'front'
    
                if vv_b[1] > d_k_kk:
                    #check kk neighbors 
                    boolean = []
                    for kkk, vvv in intersections_dict[kk_b][where].items():
                        if vvv[1] < d_k_kk:
                            #print(vvv[1], d_k_kk)
                            try:
                                d_kk_kkk = intersections_dict[kkk]['back'][kk_b][1]
                            except:
                                d_kk_kkk = intersections_dict[kkk]['front'][kk_b][1]
    
                            if d_kk_kkk > vvv[1]:
                                boolean += [0]
                            else:
                                boolean += [1]
                    #print(k,kk, boolean)
                     
                    
                    if sum(boolean) == 0:
                        #print(k, kk, back_coordinate)
                        break
        
    
        try:
            if k!= kk_f and k!= kk_b and kk_f != kk_b and (k, kk_f) not in edges and (kk_f, k) not in edges and (k, kk_b) not in edges and (kk_b, k) not in edges:                           
                segments+= [[k, kk_f, kk_b, front_coordinate[0], front_coordinate[1], back_coordinate[0], back_coordinate[1]]]
                edges += [(k,kk_f)]
                edges += [(k,kk_b)]
        except:
            None
        
    return segments

def generate_line_segments_static(size, seed_loc=None):
    if seed_loc is None:
        seed_loc = seeds(size, 0.0)
    segments = static_line_graph_generation(seed_loc, all_intersection(seed_loc))
    segments = transform_to_standard_lines(segments)
    
    return segments