import networkx as nx
import numpy as np
from typing import List

from .Classes import LineSegment

def generate_line_network(line_segments: List[LineSegment]) -> List[List[int]]:
    """
    Calculate the degree evolution of nodes in a graph over time.

    Parameters:
    - line_segments (List[LineSegment]): List of line segment objects.

    Returns:
    - List[List[int]]: List of lists representing the degree evolution at each time step.
    """
    # Create an empty graph.
    G = nx.Graph()

    # Add all segments minus the borders
    for index, segment in enumerate(line_segments):
        
        # Add a node for the current segment
        G.add_node(segment.id, loc=(np.array(segment.start) + np.array(segment.end)) / 2)
        
        # Add edges between the current segment and its neighbors.
        G.add_edges_from([(segment.id, neighbor) for neighbor in segment.neighbors_initial])
        
        # Calculate and print progress percentage
        percentage = np.round((index+1) / len(line_segments[4:]) * 100, 3)
        print(f'generate_graph: {percentage}% done', end='\r')
        
    return G