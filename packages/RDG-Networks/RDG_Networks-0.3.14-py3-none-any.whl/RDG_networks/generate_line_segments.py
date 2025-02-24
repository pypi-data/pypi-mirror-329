import math
import networkx as nx
import numpy as np
import random
from typing import List, Tuple, Union

from .Classes import Line, LineSegment, Polygon
from .sample_in_polygon import sample_in_polygon
    
def doLinesIntersect(line1: Line, line2: Line) -> Tuple[bool, Union[Tuple[float, float], None]]:
    """
    Check if two lines intersect and return the intersection point.

    Args:
    - line1 (Line): The first line segment.
    - line2 (Line): The second line segment.

    Returns:
    - intersect (bool): True if the lines intersect, False otherwise.
    - intersection_point (tuple or None): The intersection point (x, y) if lines intersect, None otherwise.
    """
    x1, y1 = line1.location
    v1, w1 = line1.direction

    x2, y2 = line2.location
    v2, w2 = line2.direction

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

def get_cyles(cycle, segment_new_id, neighbor1, neighbor2, index_begin, index_end):
    
    if index_begin < index_end:
        cycle1 = [segment_new_id] + cycle[index_begin:index_end] + [neighbor2] + [segment_new_id]
        cycle2 = [segment_new_id] + cycle[index_end:] + cycle[:index_begin] + [neighbor1] + [segment_new_id]
    else:
        cycle1 = [segment_new_id] + cycle[index_begin:] + cycle[:index_end] + [neighbor2] + [segment_new_id]
        cycle2 = [segment_new_id] + cycle[index_end:index_begin] + [neighbor1] + [segment_new_id]
    
    return cycle1, cycle2

def get_vertices(vertices, index_begin, index_end, vertex_begin, vertex_end):
    if index_begin < index_end:
        vertices1 = [vertex_begin] + vertices[index_begin:index_end] + [vertex_end]
        vertices2 = [vertex_end] + vertices[index_end:] + vertices[:index_begin] + [vertex_begin]
    else:
        vertices1 = [vertex_begin] + vertices[index_begin:] + vertices[:index_end] + [vertex_end]
        vertices2 = [vertex_end] + vertices[index_end:index_begin] + [vertex_begin]
    
    return vertices1, vertices2

def update_polygon_arr(polygon_id, polygon_arr, neighbor1, neighbor2, vertex_begin, vertex_end):
    
    vertices=polygon_arr[polygon_id]['vertices']
    cycle = polygon_arr[polygon_id]['faces']
    index_begin, index_end = (cycle.index(neighbor1), cycle.index(neighbor2))
    
    cycle1, cycle2 = get_cyles(cycle=cycle, segment_new_id=str(len(polygon_arr)), neighbor1=neighbor1, neighbor2=neighbor2, index_begin=index_begin, index_end=index_end)
    vertices1, vertices2 = get_vertices(vertices, index_begin, index_end, vertex_begin, vertex_end)

    polygon1 = Polygon(vertices=vertices1)
    area1 = polygon1.area()
    area2 = polygon_arr[polygon_id]['area'] - area1
    
    polygon_new_1 = { f'p{len(polygon_arr)+1}': { 'vertices': vertices1, 'area': area1, 'faces': cycle1[:-1] } }
    polygon_new_2 = { polygon_id: { 'vertices': vertices2, 'area': area2, 'faces': cycle2[:-1] } }

    polygon_arr.update(polygon_new_1)
    polygon_arr.update(polygon_new_2)
    
    return polygon_arr
        
def pick_item_with_probability(polygon_arr):
    threshold = random.uniform(0, 1)
    cumulative_weight = 0
    for item, pol in polygon_arr.items():
        weight = pol['area']
        cumulative_weight += weight
        if cumulative_weight >= threshold:
            return item, pol
        
def add_line_segment(segments_dict, polygon_arr, angles='uniform') -> Tuple[List[Line], List[Tuple[int, int]]]:
    """
    Add a new line segment to the list of line segments and update edge information.

    Args:
    - line_segments (List[Line]): List of existing line segments.
    - polygon_arr (List[Polygon]): List of existing polygons.
    - angles: 'uniform' or specific angles in radians compared to positive x-axis. 

    Returns:
    - Updated line_segments list.
    """    
    polygon_id, polygon = pick_item_with_probability(polygon_arr)
    
    line_segments_to_check = [segments_dict[segment] for segment in polygon['faces']]
    
    location_new = sample_in_polygon(polygon['vertices'])
    
    if angles == 'uniform':
        direction_new = (random.uniform(-1, 1), random.uniform(-1, 1))
    else:
        directions = [ (np.cos(angle), np.sin(angle)) for angle in angles ]
        direction_new = random.choice(directions)

    line_new = Line(location=location_new, direction=direction_new)
    intersection_points = []

    for segment in line_segments_to_check:
        location = np.array(segment.start)
        direction = np.array(segment.end) - np.array(segment.start)
        line = Line(location=location, direction=direction)

        intersect, (intersect_x, intersect_y) = doLinesIntersect(line_new, line)

        if not intersect:
            continue

        xcheck = (
            segment.end[0] <= intersect_x <= segment.start[0]
            or segment.start[0] <= intersect_x <= segment.end[0]
            or abs(intersect_x - segment.end[0]) < 1e-6
            or abs(intersect_x - segment.start[0]) < 1e-6
        )

        ycheck = (
            segment.end[1] <= intersect_y <= segment.start[1]
            or segment.start[1] <= intersect_y <= segment.end[1]
            or abs(intersect_y - segment.end[1]) < 1e-6
            or abs(intersect_y - segment.start[1]) < 1e-6
        )

        if intersect and xcheck and ycheck:
            segment_length = math.sqrt(
                (line_new.location[0] - intersect_x) ** 2
                + (line_new.location[1] - intersect_y) ** 2
            )
            intersection_points.append(
                {"id": segment.id, "point": (intersect_x, intersect_y), "segment_length": segment_length}
            )

    # Divide intersections in back and front of the new line
    intersections_b = [intersection for intersection in intersection_points if intersection["point"][0] < line_new.location[0]]
    intersections_f = [intersection for intersection in intersection_points if intersection["point"][0] > line_new.location[0]]
    
    if not intersections_b or not intersections_f:
        intersections_b = [intersection for intersection in intersection_points if intersection["point"][1] < line_new.location[1]]
        intersections_f = [intersection for intersection in intersection_points if intersection["point"][1] > line_new.location[1]]

    # Determine correct segment length
    id = str(len(segments_dict)-3)

    start = min(intersections_b, key=lambda x: x["segment_length"])
    end = min(intersections_f, key=lambda x: x["segment_length"])
    
    # Add new segment object with corresponding neighbors
    neighbors_initial = {}
    neighbors_initial[start["id"]] = start["point"]
    neighbors_initial[end["id"]] = end["point"]

    neighbors = {}
    neighbors[start["id"]] = start["point"]
    neighbors[end["id"]] = end["point"]
    segment_new = LineSegment(start=start["point"], end=end["point"], id=id, neighbors_initial=neighbors_initial, neighbors=neighbors)
        
    segments_dict[segment_new.id] = segment_new
    
    segments_dict[start["id"]].neighbors[id] = start["point"]
    segments_dict[end["id"]].neighbors[id] = end["point"]
    
    vertex_begin = start["point"]
    vertex_end = end["point"]
    polygon_arr = update_polygon_arr(polygon_id=polygon_id, polygon_arr=polygon_arr, neighbor1=start["id"], neighbor2=end["id"], vertex_begin=vertex_begin, vertex_end=vertex_end)
    
    return segments_dict, polygon_arr

def generate_line_segments(size: int, angles='uniform') -> Tuple[nx.Graph, List[LineSegment]]:
    """
    Generate a network of line segments with random intersections.

    Args:
    - size (int): Number of line segments to generate.

    Returns:
    - line_segments (List[LineSegment]): List of LineSegment objects.
    """
    borders = [
        LineSegment((1, 0), (0, 0), id='b1', neighbors_initial={'b2': (0, 0), 'b4': (1, 0)}, neighbors={'b2': (0, 0), 'b4': (1, 0)}),
        LineSegment((0, 1), (0, 0), id='b2', neighbors_initial={'b1': (0, 0), 'b3': (0, 1)}, neighbors={'b1': (0, 0), 'b3': (0, 1)}),
        LineSegment((0, 1), (1, 1), id='b3', neighbors_initial={'b2': (0, 1), 'b4': (1, 1)}, neighbors={'b2': (0, 1), 'b4': (1, 1)}),
        LineSegment((1, 1), (1, 0), id='b4', neighbors_initial={'b1': (1, 0), 'b3': (1, 1)}, neighbors={'b1': (1, 0), 'b3': (1, 1)})
    ]
    
    polygon_arr = { 'p1': { 'vertices': [(0,0), (0,1), (1,1), (1,0)], 'area': 1, 'faces': [ 'b1', 'b2', 'b3', 'b4' ] } }
    
    segments = borders
    segments_dict = {segment.id: segment for segment in segments}

    for i in range(size):
        segments_dict, polygon_arr = add_line_segment(segments_dict, polygon_arr, angles=angles)
        
        percentage = np.round(i / size * 100, 3)
        print(f'generate_segments: {percentage}% done', end='\r')
        
    return segments_dict, polygon_arr