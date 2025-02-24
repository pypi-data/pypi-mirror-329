import numpy as np
import math
from typing import List, Dict, Tuple
from shapely.geometry import Polygon as Polygon_Shapely
from shapely.geometry import LineString, box
from .Classes import LineSegment, Polygon

def rotate(point, center, rotation_matrix):
    """
    Rotates a point around the center using the given rotation matrix.
    point: numpy array representing the point to rotate
    center: numpy array representing the center of rotation
    rotation_matrix: 2x2 numpy array representing the rotation matrix
    """
    translated_point = point - center

    # rotated_point = np.dot(rotation_matrix, translated_point)
    rotated_point = rotation_matrix@translated_point
    final_point = rotated_point + center

    return final_point

def unit_vector(v):
    """ Returns the unit vector of the vector. """
    return v / np.linalg.norm(v)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'."""
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def get_alignment_mean(line_vector_arr, director):
    """Get the mean alignment."""
    S_all = 0
    total_mass = 0
    for item in line_vector_arr:
        line_vector = item['line_vector']
        vector_diff = np.array(line_vector[1]) - np.array(line_vector[0])

        area = item['area']
        align = math.cos(angle_between(vector_diff, director))**2
        S_all += align*area
        total_mass += area

    output = S_all / total_mass

    return output

def compute_alignment(
    angle: float, 
    segment_thickness_dict: dict[str, Polygon],
    director: np.ndarray, 
    box_measurements: list[list[float]]
) -> tuple[float, float]:
    """
    Computes the alignment of a network of segments for a given rotation angle.

    This function rotates a network of segments based on the specified angle, clips the network to fit within the 
    specified bounding box, and then calculates the alignment of the network relative to a director vector.

    Parameters:
    -----------
    angle : float
        The angle (in radians or degrees, depending on your implementation) by which to rotate the network of segments.
    segment_thickness_dict : dict[str, object]
        A dictionary where the keys are segment IDs (as strings) and the values are objects representing segments 
        (should include properties like `middle_segment` and `area()`).
    director : np.ndarray
        A numpy array representing the director vector, typically a unit vector used for calculating the alignment.
    box_measurements : list[list[float]]
        A list containing the measurements of the bounding box. It typically contains four corner points as 
        sublists, with each sublist representing [x, y] coordinates of a corner.

    Returns:
    --------
    tuple[float, float]
        A tuple where the first element is the input angle and the second element is the computed alignment value.
    """
    box_center = np.array((box_measurements[0]) + np.array(box_measurements[2])) / 2

    # Rotate network
    segment_thickness_dict_new = rotate_network(segment_thickness_dict, rotate_angle=angle, box_center=box_center)

    # Clip network
    segment_thickness_dict_new = clip_network(segment_thickness_dict_new, box_measurements=box_measurements)

    line_vectors = [
        {'line_vector': [seg.middle_segment.start, seg.middle_segment.end], 'area': seg.area()}
        for seg in segment_thickness_dict_new.values() if seg.middle_segment is not None
    ]

    alignment = get_alignment_mean(line_vectors, director)
    
    return angle, alignment

def get_max_alignment(
    segment_thickness_dict: dict, 
    director: np.ndarray, 
    box_measurements: list[float], 
    grid_points: int = 360
) -> float:
    """Find the angle with the maximum alignment using parallel processing."""
    # Create a list of angles to evaluate
    angles = np.linspace(0, np.pi, grid_points)

    results = []
    for a in angles:
        result = compute_alignment(a, segment_thickness_dict, director, box_measurements)
        results.append(result)

    # Find the angle with the maximum alignment
    max_alignment = 0
    max_angle = None
    for angle, alignment in results:
        if alignment > max_alignment:
            max_alignment = alignment
            max_angle = angle

    return max_angle

def rotate_network(
    segment_thickness_dict: dict[str, Polygon],
    rotate_angle: float, 
    box_center: Tuple[float, float]
) -> dict[str, object]:
    """
    Rotates a network of line segments around a given center point.

    This function rotates each segment in the provided network by a specified angle around the center of a bounding box.
    The segments are represented by their vertices and a middle segment, and both are transformed using a rotation matrix.

    Parameters:
    -----------
    segment_thickness_dict : dict[str, object]
        A dictionary where the keys are segment IDs (as strings) and the values are segment objects. Each segment 
        object must have a `vertices` attribute (list of vertex coordinates) and a `middle_segment` attribute.
    rotate_angle : float
        The angle in radians by which to rotate the network of segments.
    box_center : Tuple[float, float]
        The (x, y) coordinates representing the center point around which to rotate the network.

    Returns:
    --------
    dict[str, object]
        A new dictionary with rotated segments, where the keys are the same segment IDs and the values are the 
        transformed segment objects with updated vertices and middle segments.
    """
    # Define the center and rotation matrix for rotation
    center = np.array([box_center[0], box_center[1]])
    rotation_matrix = np.array([[np.cos(rotate_angle), -np.sin(rotate_angle)], 
                                [np.sin(rotate_angle), np.cos(rotate_angle)]])

    # Create a new dictionary to store the rotated segments
    segment_thickness_dict_new = {}

    # Iterate over each segment and apply the rotation
    for id, segment in segment_thickness_dict.items():
        vertices_new = []
        # Rotate each vertex of the segment
        for v in segment.vertices:
            v_rotate = rotate(v, center, rotation_matrix)
            vertices_new.append(v_rotate)

        # Rotate the start and end points of the middle segment
        start = rotate(segment.middle_segment.start, center, rotation_matrix)
        end = rotate(segment.middle_segment.end, center, rotation_matrix)

        # Create a new middle segment with rotated coordinates
        middle_segment_new = LineSegment(start=start, end=end)
        
        # Store the rotated segment in the new dictionary
        segment_thickness_dict_new[id] = Polygon(vertices=vertices_new, middle_segment=middle_segment_new, neighbors=segment.neighbors)

    return segment_thickness_dict_new

def clip_network(
    segment_thickness_dict: dict[str, Polygon],
    box_measurements: list[list[float]]
) -> dict[str, object]:
    """
    Clips the segments in the network to fit within a bounding box.

    This function clips each segment in the network so that only the portions that lie inside the bounding box are retained. 
    The bounding box is represented as a polygon, and any segment that intersects the box is clipped to the intersection area.

    Parameters:
    -----------
    segment_thickness_dict : dict[str, object]
        A dictionary where the keys are segment IDs (as strings) and the values are segment objects. Each segment 
        object must have a `vertices` attribute (list of vertex coordinates) and a `middle_segment` attribute.
    box_measurements : list[list[float]]
        A list of 4 sublists, each representing the [x, y] coordinates of a corner of the bounding box.

    Returns:
    --------
    dict[str, object]
        A dictionary containing the clipped segments, where the keys are the same segment IDs and the values are the 
        clipped segment objects with updated vertices and middle segments.
    """
    # Create a Shapely Polygon from the bounding box measurements
    box_new = Polygon_Shapely([
        (box_measurements[0][0], box_measurements[0][1]), 
        (box_measurements[1][0], box_measurements[1][1]), 
        (box_measurements[2][0], box_measurements[2][1]), 
        (box_measurements[3][0], box_measurements[3][1])
    ])

    # Dictionary to store the clipped segments
    segment_thickness_dict_new = {}

    # Iterate over each segment
    for id, segment in enumerate(segment_thickness_dict.values()):
        vertices_new = []
        vertices = segment.vertices

        # Create a Shapely polygon for the segment's vertices
        pol = Polygon_Shapely(vertices)

        # Find the intersection between the segment's polygon and the bounding box
        intersection = box_new.intersection(pol)
        if not intersection.is_empty:
            # If there is an intersection, retrieve the clipped vertices
            vertices_new = list(intersection.exterior.coords)
  
        if vertices_new:
            # If new vertices exist, clip the middle segment as well
            start = segment.middle_segment.start
            end = segment.middle_segment.end

            middle_segment_new = None
            # Find the intersection between the middle segment and the bounding box
            intersection = box_new.intersection(LineString([start, end]))
            if not intersection.is_empty:
                start = list(intersection.coords)[0]
                end = list(intersection.coords)[-1]
                middle_segment_new = LineSegment(start=start, end=end)

            # Create a new clipped polygon with updated vertices and middle segment
            pol_new = Polygon(vertices=vertices_new, middle_segment=middle_segment_new, neighbors=segment.neighbors)
            pol_new.sort_vertices()  # Ensure vertices are sorted
            segment_thickness_dict_new[id] = pol_new

    return segment_thickness_dict_new

def translate_network(
    segment_thickness_dict: dict[str, Polygon],
    translation_vector: np.ndarray
) -> dict[str, object]:
    """
    Translates a network of line segments by a given translation vector.

    This function moves each segment in the network by applying the translation vector to the coordinates of the vertices
    and the start and end points of the middle segment (if it exists).

    Parameters:
    -----------
    segment_thickness_dict : dict[str, object]
        A dictionary where the keys are segment IDs (as strings) and the values are segment objects. Each segment 
        object must have `vertices` (list of vertex coordinates) and `middle_segment` attributes.
    translation_vector : np.ndarray
        A 2D numpy array representing the translation vector [x, y] that will be applied to all the vertices and 
        middle segments of each segment.

    Returns:
    --------
    dict[str, object]
        A new dictionary with the translated segments, where the keys are the same segment IDs and the values are 
        the translated segment objects.
    """
    # Create a new dictionary to store the translated segments
    segment_thickness_dict_new = {}

    # Iterate over each segment and apply the translation
    for id, segment in segment_thickness_dict.items():
        # Translate the vertices by adding the translation vector to each vertex
        vertices_new = [np.array(v) + translation_vector for v in segment.vertices]
        
        # Check if the segment has a middle segment to translate
        if segment.middle_segment is None:
            middle_segment_new = None
        else:
            start = segment.middle_segment.start + translation_vector
            end = segment.middle_segment.end + translation_vector
            middle_segment_new = LineSegment(start=start, end=end)
        
        # Store the translated segment in the new dictionary
        segment_thickness_dict_new[id] = Polygon(vertices=vertices_new, middle_segment=middle_segment_new, neighbors=segment.neighbors)

    return segment_thickness_dict_new

def orientate_network(
    data_dict: Dict[str, dict], 
    orientation: List[int], 
    grid_points: int = 360, 
    box_measurements: List[Tuple[float, float]] = [(0, 0), (0, 1), (1, 1), (1, 0)],
    director: np.ndarray = np.array([0, 1])
) -> List[Dict[str, dict]]:
    """
    Generates a set of networks of line segments with different thicknesses and orientations, and clips them to fit 
    within a bounding box. The function also aligns the network to the maximum alignment angle with respect to the y-axis.

    Parameters:
    -----------
    data_dict : Dict[str, dict]
        A dictionary containing the initial network data. Must include the key 'segment_thickness_dict', which holds
        the segment information.
    orientation : List[int]
        A list of orientations (angles in degrees or radians) to rotate the network. For each orientation, the network
        is regenerated and rotated.
    grid_points : int, optional
        The number of grid points for calculating the maximum alignment angle (default is 360).
    box_measurements : List[Tuple[float, float]], optional
        A list of tuples representing the corner points of the bounding box (default is a unit square).

    Returns:
    --------
    List[Dict[str, dict]]
        A list of dictionaries. Each dictionary contains the 'orientation' of the network and the updated 'data_dict' 
        with the rotated and clipped segment information.
    """
    
    # Compute the center of the box
    box_center = (np.array(box_measurements[0]) + np.array(box_measurements[2])) / 2
    
    # Extract the segment thickness dictionary from the input data
    segment_thickness_dict = data_dict['segment_thickness_dict']
    
    # Find the angle that aligns the network most with the y-axis
    max_angle = get_max_alignment(segment_thickness_dict, director, box_measurements, grid_points)
    
    # Store the initial unmodified configuration
    output = [{'orientation': 'original', 'data_dict': data_dict}]
    
    # Loop through each given orientation, rotate, clip, and translate the network
    for o in orientation:
        # Compute the rotation angle for the current orientation relative to max alignment
        rotate_angle = -max_angle + o
        
        # Rotate the network by the computed angle
        segment_thickness_dict_rotated = rotate_network(segment_thickness_dict, rotate_angle=rotate_angle, box_center=box_center)

        # Clip the rotated network to fit within the bounding box
        segment_thickness_dict_clipped = clip_network(segment_thickness_dict_rotated, box_measurements=box_measurements)

        # Translate the clipped network to start at the origin (0,0)
        translation_vector = -np.array(box_measurements[0])
        segment_thickness_dict_translated = translate_network(segment_thickness_dict_clipped, translation_vector)
    
        # Prepare a new data dictionary with the transformed segment information
        data_dict_new = {
            'segments_dict': None,
            'polygon_arr': None,
            'segment_thickness_dict': segment_thickness_dict_translated,
            'jammed': None,
            'generated_config': None
        }
        
        # Append the result for this orientation
        output.append({'orientation': o, 'data_dict': data_dict_new})
    
    return output