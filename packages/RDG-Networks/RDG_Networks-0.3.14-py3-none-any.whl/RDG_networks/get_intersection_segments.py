import numpy as np
from typing import List, Tuple

from .Classes import LineSegment

def order_points(points: List[Tuple[float, float]], segment_start: Tuple[float, float]) -> List[Tuple[float, float]]:
    """
    Orders a list of points based on their distance from a given starting point.

    Args:
    - points (List[Tuple[float, float]]): List of points to be ordered.
    - segment_start (Tuple[float, float]): Starting point to calculate distances from.

    Returns:
    - ordered_points (List[Tuple[float, float]]): Points ordered by their distance from segment_start.
    """
    distances = [(i, np.linalg.norm(np.array(point) - np.array(segment_start))) for i, point in enumerate(points)]
    distances.sort(key=lambda x: x[1])
    ordered_points = [points[i] for i, _ in distances]
    return ordered_points

def get_intersection_segments(line_segments: List[LineSegment]) -> List[LineSegment]:
    """
    Generates intersection segments between a list of line segments.

    Args:
    - line_segments (List[LineSegment]): List of line segments.

    Returns:
    - intersection_segments (List[LineSegment]): List of intersection segments.
    """
    intersection_points = {segment.id: [] for segment in line_segments}

    intersection_points['b1'] = [(1, 0), (0, 0)] 
    intersection_points['b2'] = [(0, 1), (0, 0)] 
    intersection_points['b3'] = [(0, 1), (1, 1)] 
    intersection_points['b4'] = [(1, 1), (1, 0)] 

    # Add all segments minus the borders
    for index, segment in enumerate(line_segments):
        if segment.id in ['b1', 'b2', 'b3', 'b4']:
            continue

        neighbors_initial = segment.neighbors_initial

        # Add segment start and end points to intersection points
        intersection_points[segment.id].append(segment.start)
        intersection_points[segment.id].append(segment.end)

        # Add neighboring points to intersection points
        for neighbor_id, neighbor_point in neighbors_initial.items():
            intersection_points[neighbor_id].append(neighbor_point)

    # Order intersection points
    ordered_intersection_points = {}
    for segment_id, points in intersection_points.items():
    
        ordered_points = order_points(points, points[0])
        ordered_points = list(set(ordered_points))
        ordered_intersection_points[segment_id] = ordered_points

    # Generate intersection segments
    intersection_segments = []
    i = 1
    for _, points in ordered_intersection_points.items():
        for index in range(1, len(points)):
            id = str(i)
            start = points[index - 1]
            end = points[index]

            segment_new = LineSegment(start=start, end=end, id=id)
            intersection_segments.append(segment_new)
            i += 1

    return intersection_segments