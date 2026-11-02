"""
Coating Evaluation

Image processing and evaluation tools for measuring coating thickness.

Public API:
- calculation: Calculate coating thickness from images.
- edges_and_areas: Extract coating regions and edges.
- evaluation: Evaluate and visualize coating thickness results.
"""

__version__ = "0.1.0"

from .evaluation import evaluation
from .calculation import edges_and_areas,calculation

__all__=["__version__","evaluation","edges_and_areas","calculation"]