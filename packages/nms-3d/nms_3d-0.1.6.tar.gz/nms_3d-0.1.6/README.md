# 3D Non-Maximum Suppression

A package for performing 3D Non-Maximum Suppression (NMS) on 3D bounding boxes and plotting them in 3D space.

## Installation
Install the package running:
```bash
pip install nms-3d
```

## Import
Import the package as:
```python
import nms_3d
```

## Package organization

The package consists of the following Python modules:

- **plot_3d_boxes**: function for creating 3D plots as .html files containing bounding boxes created with Plotly.
- **nms_3d**: function that apply the NMS 3D algorithm on the input bounding boxes.


## Requirements

```
Python>=3.9.5
torch>=2.2.2
plotly>=5.13.1
```
