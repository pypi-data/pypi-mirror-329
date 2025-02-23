# image_converter

A Python package for optimizing images and converting them to WebP format.

## Installation

```bash
pip install image_converter
```

### Usage

```python

from image_converter import ImageOptimizer

# Create an optimizer instance
optimizer = ImageOptimizer(quality=85)

# Convert a single image
optimizer.convert_to_webp('input.jpg', 'output.webp')

# Convert all images in a folder
optimizer.batch_optimize('input_folder', 'output_folder')

```

### Features

- Convert images to WebP format
- Batch processing support
- Quality control for optimization
- Handles RGBA images
- Supports PNG, JPG, JPEG, TIFF, BMP formats


### License
MIT License
