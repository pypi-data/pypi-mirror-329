import numpy as np
import random
from shapely.geometry import LineString
from typing import List, Dict, Any, Tuple
import matplotlib.pyplot as plt

from .Classes import LineSegment

def grow_lines(lines: List[Dict[str, Any]], epsilon: float) -> List[Dict[str, Any]]:
    """
    Grows lines based on their current status.

    Args:
        lines (List[Dict[str, Any]]): A list of dictionaries representing lines, each containing keys
            'growth_status', 'end', and 'angle'.
        epsilon (float): The amount by which to grow the lines.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries representing the updated lines after growth.
    """
    for index, line in enumerate(lines):
        if line['growth_status']:
            # Update the end point of the line based on epsilon and angle
            lines[index]['end'] = (
                line['end'][0] + epsilon * np.cos(line['angle']),
                line['end'][1] + epsilon * np.sin(line['angle'])
            )
    
    return lines

def add_new_line(lines: List[Dict[str, Any]], line_id: str, t_total: float, angles='uniform') -> List[Dict[str, Any]]:
    """
    Adds a new line and its mirror line to the list of lines.

    Args:
        lines (List[Dict[str, Any]]): A list of dictionaries representing existing lines.
        line_id (str): The identifier for the new line.
        t_total (float): The total time elapsed.
        angles (str) or List: The allowed anfles in the system.

    Returns:
        List[Dict[str, Any]]: The updated list of lines after adding the new line and its mirror line.
    """
    np_x = random.uniform(0, 1)
    np_y = random.uniform(0, 1)
    
    if angles == 'uniform':
        angle = random.uniform(-np.pi, np.pi)
        
    else: 
        angle = random.choice(angles)

    # Create the first line
    line_new_1 = {
        'id': f'{line_id}_1',
        'introduction_time': t_total,
        'neighbors_initial': [],
        'start': (np_x, np_y),
        'end': (np_x, np_y),
        'angle': angle,
        'growth_status': True
    }

    # Create the mirror line
    line_new_2 = line_new_1.copy()
    line_new_2['id'] = f'{line_id}_2'
    line_new_2['angle'] = angle + np.pi

    # Add both lines to the list
    lines.extend([line_new_1, line_new_2])
    
    return lines

def update_for_border_intersections(lines: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Update lines that intersect with the border.

    Args:
        lines (List[Dict[str, Any]]): A list of dictionaries representing lines.

    Returns:
        List[Dict[str, Any]]: The updated list of lines after handling border intersections.
    """
    for index, line in enumerate(lines):
        if lines[index]['growth_status'] == True and (line['end'][0] < 0 or line['end'][0] > 1 or line['end'][1] < 0 or line['end'][1] > 1):
            # If line has intersected with the border, update its properties
            lines[index]['neighbors_initial'] = lines[index]['neighbors_initial'] + ['border']
            lines[index]['growth_status'] = False
            
    return lines

def check_and_update_when_intersect(lines: List[Dict[str, Any]], epsilon: float, dt: float) -> List[Dict[str, Any]]:
    """
    Check for intersections between lines and update their properties accordingly.

    Args:
        lines (List[Dict[str, Any]]): A list of dictionaries representing lines.
        epsilon (float): The growth rate of the lines.

    Returns:
        List[Dict[str, Any]]: The updated list of lines after handling intersections.
    """
        
    for index1, j1 in enumerate(lines):
        for index2, j2 in enumerate(lines):
            if j1['id'][:-2] == j2['id'][:-2] or index2 < index1:
                continue
            
            if j1['growth_status'] == False and j2['growth_status'] == False:
                continue
            
            line1 = LineString([j1['start'], j1['end']])
            line2 = LineString([j2['start'], j2['end']])
            
            intersection_pt = line1.intersection(line2)

            if not intersection_pt.is_empty:
                d1 = np.linalg.norm(np.array(j1['start']) - np.array([intersection_pt.x, intersection_pt.y]))
                d2 = np.linalg.norm(np.array(j2['start']) - np.array([intersection_pt.x, intersection_pt.y]))
                
                arrival_1 = j1['introduction_time'] + d1 / epsilon * dt
                arrival_2 = j2['introduction_time'] + d2 / epsilon * dt

                if arrival_1 > arrival_2:
                    lines[index1]['end'] = (intersection_pt.x, intersection_pt.y)
                    lines[index1]['neighbors_initial'] = lines[index1]['neighbors_initial'] + [j2['id'][:-2]]
                    lines[index1]['growth_status'] = False                    

                else:                        
                    lines[index2]['end'] = (intersection_pt.x, intersection_pt.y)
                    lines[index2]['neighbors_initial'] = lines[index2]['neighbors_initial'] + [j1['id'][:-2]]
                    lines[index2]['growth_status'] = False

    return lines

def transform_to_standard_lines(lines: List[Dict[str, Any]]) -> List[LineSegment]:
    """
    Transform a list of lines into a list of standard line segments.

    Args:
        lines (List[Dict[str, Any]]): A list of dictionaries representing lines.

    Returns:
        List[LineSegment]: A list of LineSegment objects representing standard line segments.
    """
    segments = []
    for index in range(0, len(lines), 2):
        s1 = lines[index]
        s2 = lines[index + 1]
        
        id = s1['id'][:-2]
        start = s1['end']
        end = s2['end']
        
        neighbors = [s1['neighbors_initial'], s2['neighbors_initial']]
        
        line_segment = LineSegment(start=start, end=end, id=id, neighbors_initial=neighbors)
        segments.append(line_segment)
        
    return segments

def generate_line_segments_dynamic(size: int, dt: float, epsilon: float, time: float, angles='uniform') -> List[LineSegment]:
    """
    Generate line segments dynamically based on growth and intersection conditions.

    Args:
        size (int): The desired number of line segments.
        dt (float): Time increment.
        epsilon (float): Growth rate of the lines.
        time (float): Interval at which new lines are added.
        angles (str or List): The allowed angles in the system (default is 'uniform' for random angles).

    Returns:
        List[LineSegment]: A list of LineSegment objects representing standard line segments.
    """
    lines = []
    line_id, t, t_total = 1, 0, 0
    
    # Stop loop whenever we have enough lines and all lines have stopped growing
    while len(lines) / 2 < size or np.any([item['growth_status'] for item in lines]):

        t += dt
        t_total += dt
        
        if t > time and len(lines) / 2 < size:
            
            if time == 0:
                number_of_lines_to_add = size
            else:
                number_of_lines_to_add = int(t / time)
                
            for _ in range(number_of_lines_to_add):
                lines = add_new_line(lines, line_id, t_total, angles=angles)
                line_id += 1
                
            t = 0

        lines = grow_lines(lines, epsilon)
        lines = update_for_border_intersections(lines)
        lines = check_and_update_when_intersect(lines, epsilon, dt)
        
    lines = transform_to_standard_lines(lines)
        
    return lines