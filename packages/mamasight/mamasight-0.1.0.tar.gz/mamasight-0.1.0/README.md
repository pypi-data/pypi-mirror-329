# MamaSight

MamaSight is a Python package for analyzing images using YOLO object detection and OCR (Optical Character Recognition). It's designed to detect UI elements and text in screenshots and provide annotated visualizations.

## Installation

```bash
pip install mamasight
```

## Dependencies

MamaSight depends on the following packages:

- torch & torchvision
- ultralytics (v8.3.70)
- numpy (v1.26.4)
- OpenCV
- PaddlePaddle & PaddleOCR (optional for OCR)
- EasyOCR (fallback OCR)
- pandas

## Usage

```python
from mamasight import ScreenParser

# Custom box annotation settings (optional)
box_config = {
    'box_overlay_ratio': 3200,  # Base ratio for scaling
    'text_scale': 1.0,          # Scale factor for text
    'text_thickness': 3,        # Thickness of text
    'text_padding': 5,          # Padding around text
    'thickness': 4,             # Thickness of bounding boxes
    'annotation_style': 'simple', # 'simple' or 'colorful'
}

# Initialize parser with custom settings
parser = ScreenParser(box_config=box_config)

# Setup (will auto-detect GPU/CPU if not specified)
parser.setup(yolo_device='cuda', ocr_device='cuda')  # or 'cpu' for CPU

# Analyze image (with or without OCR)
image, detections = parser.analyze('screenshot.png', use_ocr=True)

# Display the annotated image
image.show()

# View detection results as a pandas DataFrame
print(detections)
```

## Features

- Detect UI elements (icons, buttons, etc.) using YOLO
- Optional text detection with OCR
- Customizable annotation styles
- Auto GPU/CPU detection
- Returns both annotated image and structured detection data

## License

MIT
