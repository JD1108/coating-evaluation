# coating-evaluation v0.1.0


A Python library for evaluating coating thickness on high contrast grayscale images.


## Installation


```bash

pip install coating-evaluation

```


## Quick Start


### Paket


```python

from coating_evaluation.calculation import calculation

gray, coating, skel, means, stds=calculation(img_path,width,res)

```


### Command Line Interface


Display available options:

```bash

coating-evaluation --help

```


## API Documentation


_This section is automatically generated from docstrings._


### `coating_evaluation`


Coating Evaluation

Image processing and evaluation tools for measuring coating thickness.

Public API:
- calculation: Calculate coating thickness from images.
- edges_and_areas: Extract coating regions and edges.
- evaluation: Evaluate and visualize coating thickness results.


#### `calculation()`


Calculating Coating thickness by measure the distance between the center contour (skelet) and the edge.


#### `edges_and_areas()`


Extract Coating and the edges from a grayscale image


#### `evaluation()`


Only the evaluation of the calculated data, and a comparison to measured by hand data.


## License


Apache-2.0
