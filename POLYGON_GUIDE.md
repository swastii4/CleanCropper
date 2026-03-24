# Polygon Segmentation to Bounding Box Cropper

Your labels are **polygon segmentation** format! This script converts those polygons to bounding boxes and crops the objects.

## Your Label Format

Each line in your txt files:
```
class_id x1 y1 x2 y2 x3 y3 x4 y4 ...
```

Example from your file:
```
0 0.185546875 0.185546875 0.130859375 0.185546875 0.130859375 0.267578125 0.185546875 0.267578125
```

This means:
- Class: 0
- Polygon with 4 points: (0.185, 0.185), (0.130, 0.185), (0.130, 0.267), (0.185, 0.267)
- Coordinates are **normalized** (0-1 range, multiply by image width/height to get pixels)

## What This Script Does

1. ✅ Reads polygon coordinates from txt files
2. ✅ Finds min/max x,y to create bounding box
3. ✅ Converts normalized coords to pixels
4. ✅ Crops the bounding box area
5. ✅ Saves as separate images

## Example Conversion

Polygon points: `(100,50), (150,50), (150,100), (100,100)`
↓
Bounding box: `x1=100, y1=50, x2=150, y2=100`
↓
Cropped image: 50x50 pixels

## Usage

1. Install: `pip install Pillow`

2. Edit script:
```python
ZIP_FILE = "your_dataset.zip"
OUTPUT = "cropped_objects"
```

3. Run: `python polygon_crop.py`

## Output

Files named: `imagename_class0_obj1.jpg`, `imagename_class0_obj2.jpg`, etc.

The bounding box tightly fits around the polygon!
