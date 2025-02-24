import matplotlib.pyplot as plt
from typing import List, Optional

from .Classes import LineSegment

def draw_segments(segments: List[LineSegment], fig: Optional[plt.Figure] = None, ax: Optional[plt.Axes] = None) -> None:
    """
    Draw the line segments on a matplotlib plot.

    Args:
    - line_segments (List[LineSegment]): List of LineSegment objects.
    - fig (Optional[plt.Figure]): Matplotlib figure to use for the plot.
    - ax (Optional[plt.Axes]): Matplotlib axes to use for the plot.
    """
    if fig is None:
        fig, ax = plt.subplots()

    for segment in segments:
        segment.draw(ax=ax)

    ax.hlines(0, 0, 1, color='black')
    ax.hlines(1, 0, 1, color='black')
    ax.vlines(0, 0, 1, color='black')
    ax.vlines(1, 0, 1, color='black')

    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    ax.set_xticks([])
    ax.set_yticks([])