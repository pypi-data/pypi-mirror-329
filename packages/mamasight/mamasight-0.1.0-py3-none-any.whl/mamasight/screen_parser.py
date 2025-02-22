import torch
import numpy as np
import cv2
from PIL import Image
from typing import Dict, List, Tuple, Optional
import pandas as pd
from pathlib import Path
import torch.cuda
import time
import os

class ScreenParser:
    def __init__(self, box_config: Optional[Dict] = None, weights_path: Optional[str] = None):
        """
        Initialize the Screen Parser with optional box configuration.

        Args:
            box_config: Dictionary containing box annotation settings
                - annotation_style: 'simple' (default) or 'colorful'
                - box_overlay_ratio: Base ratio for scaling (default: 3200)
                - text_scale: Scale factor for text (default: 0.8)
                - text_thickness: Thickness of text (default: 2)
                - text_padding: Padding around text (default: 3)
                - thickness: Thickness of bounding boxes (default: 3)
            weights_path: Optional custom path for storing model weights
                         If not provided, uses ~/.mamasight/weights by default
        """
        # Use user-specified path or default to home directory
        if weights_path is not None:
            self.weights_path = Path(weights_path)
        else:
            self.weights_path = Path.home() / '.mamasight' / 'weights'
        
        self.yolo = None
        self.ocr = None
        self.reader = None
        default_config = {
            'annotation_style': 'simple',
            'box_overlay_ratio': 3200,
            'text_scale': 0.8,
            'text_thickness': 2,
            'text_padding': 3,
            'thickness': 3
        }
        self.box_config = {**default_config, **(box_config or {})}
        self._is_setup = False
        self._use_paddle = False
        self.yolo_device = None
        self.ocr_device = None

    def setup(self, yolo_device: str = None, ocr_device: str = None) -> bool:
        """
        Set up the parser with specified devices for YOLO and OCR.

        Args:
            yolo_device: Device for YOLO model ('cuda' or 'cpu'). Auto-detected if not specified.
            ocr_device: Device for OCR model ('cuda' or 'cpu'). Auto-detected if not specified.
                       Set to None to disable OCR functionality.
                
        Returns:
            bool: True if setup was successful, False otherwise.
        """
        if self._is_setup:
            print("Parser is already set up")
            return True

        # Auto-detect devices if not specified
        if yolo_device is None:
            yolo_device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
        self.yolo_device = yolo_device
        self.ocr_device = ocr_device

        try:
            # Create weights directory
            self.weights_path.mkdir(exist_ok=True, parents=True)
            
            # Set up YOLO model
            yolo_setup_success = self._setup_yolo()
            if not yolo_setup_success:
                return False
            
            # Set up OCR if ocr_device is not None
            if ocr_device is not None:
                ocr_setup_success = self._setup_ocr()
                if not ocr_setup_success:
                    print("Warning: OCR setup failed, but continuing with YOLO-only functionality")
            
            self._is_setup = True
            return True

        except Exception as e:
            print(f"Setup failed: {e}")
            return False

    def _setup_yolo(self) -> bool:
        """
        Set up YOLO model using direct download only.
        
        Returns:
            bool: True if setup was successful, False otherwise.
        """
        model_path = self.weights_path / 'icon_detect' / 'model.pt'
        
        # Check if YOLO model already exists
        if model_path.exists():
            print(f"Found existing YOLO model at {model_path}, skipping download.")
        else:
            print("YOLO model not found. Downloading model weights...")
            
            # Create icon_detect directory if it doesn't exist
            (self.weights_path / 'icon_detect').mkdir(exist_ok=True, parents=True)
            
            # Direct download only (no huggingface-cli attempt)
            import requests
            
            url = "https://huggingface.co/microsoft/OmniParser-v2.0/resolve/main/icon_detect/model.pt"
            try:
                response = requests.get(url, stream=True)
                response.raise_for_status()
                
                total_size = int(response.headers.get('content-length', 0))
                block_size = 8192
                downloaded = 0
                
                with open(model_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=block_size):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            if total_size > 0:
                                percent = downloaded / total_size * 100
                                print(f"\rDownload progress: {percent:.1f}%", end="")
                print("\nYOLO model download completed.")
            except Exception as e:
                print(f"Failed to download YOLO model: {e}")
                return False
        
        if not model_path.exists():
            print("Failed to download model weights")
            return False
        
        print(f"Using YOLO model at {model_path}")

        # Initialize YOLO
        try:
            from ultralytics import YOLO
            self.yolo = YOLO(str(model_path))
            
            if self.yolo_device == 'cpu':
                self.yolo.cpu()
                print("YOLO model loaded on CPU")
            else:
                self.yolo.cuda()
                print("YOLO model loaded on GPU")
            return True
        except Exception as e:
            print(f"Failed to initialize YOLO model: {e}")
            return False

    def _setup_ocr(self) -> bool:
        """
        Set up OCR engines but don't run inference during setup.
        This matches the original working behavior.
        
        Returns:
            bool: True if setup was successful, False otherwise.
        """
        print(f"Setting up OCR on device: {self.ocr_device}")
        
        # Create OCR models directory
        ocr_model_dir = self.weights_path / 'ocr_models'
        ocr_model_dir.mkdir(exist_ok=True, parents=True)
        
        # Try PaddleOCR first
        try:
            from paddleocr import PaddleOCR
            print("Initializing PaddleOCR...")
            
            # Just initialize PaddleOCR but DON'T run inference
            # This is the key difference from your current code
            self.ocr = PaddleOCR(
                use_gpu=(self.ocr_device == 'cuda'),
                lang='en',
                use_angle_cls=False,
                show_log=True,  # Show logs during initialization
                use_dilation=True,
                det_model_dir=str(ocr_model_dir / 'det'),
                rec_model_dir=str(ocr_model_dir / 'rec')
            )
            
            self._use_paddle = True
            print("PaddleOCR setup completed.")
            return True
        except Exception as e:
            print(f"PaddleOCR initialization failed: {e}, falling back to EasyOCR")
            
            # Fall back to EasyOCR
            try:
                import easyocr
                print("Initializing EasyOCR...")
                
                # Set model storage directory
                os.environ['EASYOCR_MODULE_PATH'] = str(ocr_model_dir)
                
                # Just initialize EasyOCR but DON'T run inference
                self.reader = easyocr.Reader(
                    ['en'],
                    gpu=(self.ocr_device == 'cuda'),
                    model_storage_directory=str(ocr_model_dir),
                    download_enabled=True,
                    verbose=True
                )
                
                self._use_paddle = False
                print("EasyOCR setup completed.")
                return True
            except Exception as e:
                print(f"EasyOCR initialization also failed: {e}")
                print("OCR will not be available.")
                return False

    def _process_ocr(self, image: np.ndarray, w: int, h: int) -> List[Dict]:
        """
        Process image with OCR and return detected boxes
        
        Args:
            image: Image as numpy array
            w: Image width
            h: Image height
            
        Returns:
            List of detected text boxes
        """
        boxes = []

        if self.ocr_device is None:
            print("OCR is disabled. No text detection will be performed.")
            return boxes

        if self._use_paddle:
            ocr_results = self.ocr.ocr(image, cls=False)
            # Handle different PaddleOCR result formats
            if ocr_results and isinstance(ocr_results, list):
                if len(ocr_results) > 0:
                    # Handle case where results are in first element
                    if isinstance(ocr_results[0], list):
                        ocr_results = ocr_results[0]
                    
                    for idx, res in enumerate(ocr_results):
                        if res[1][1] > 0.9:  # Confidence threshold
                            box = res[0]
                            try:
                                x1, y1 = float(box[0][0]), float(box[0][1])
                                x3, y3 = float(box[2][0]), float(box[2][1])

                                x1, x3 = min(max(x1, 0), w), min(max(x3, 0), w)
                                y1, y3 = min(max(y1, 0), h), min(max(y3, 0), h)

                                boxes.append({
                                    'box_id': f'text_{idx}',
                                    'box_type': 'text',
                                    'content': res[1][0],
                                    'bbox': [x1/w, y1/h, x3/w, y3/h],
                                    'confidence': float(res[1][1]),
                                    'interactivity': False,
                                    'source': 'paddle_ocr'
                                })
                            except (TypeError, IndexError) as e:
                                print(f"Error processing OCR result {idx}: {e}")
                                continue
        else:
            results = self.reader.readtext(image, paragraph=False)
            for idx, (coords, text, conf) in enumerate(results):
                if conf > 0.9:  # Confidence threshold
                    x1, y1 = float(coords[0][0]), float(coords[0][1])
                    x3, y3 = float(coords[2][0]), float(coords[2][1])

                    x1, x3 = min(max(x1, 0), w), min(max(x3, 0), w)
                    y1, y3 = min(max(y1, 0), h), min(max(y3, 0), h)

                    boxes.append({
                        'box_id': f'text_{idx}',
                        'box_type': 'text',
                        'content': text,
                        'bbox': [x1/w, y1/h, x3/w, y3/h],
                        'confidence': float(conf),
                        'interactivity': False,
                        'source': 'easy_ocr'
                    })
        
        print(f"OCR processing completed. Found {len(boxes)} text elements.")
        return boxes

    def _annotate_image(self, image: np.ndarray, boxes: List[Dict], w: int, h: int) -> np.ndarray:
        """
        Annotate image with bounding boxes.
        
        Args:
            image: Image as numpy array
            boxes: List of detected boxes
            w: Image width
            h: Image height
            
        Returns:
            Annotated image as numpy array
        """
        annotation_style = self.box_config.get('annotation_style', 'simple')
        # Configure annotation parameters based on box_config and image size
        box_overlay_ratio = max(w, h) / self.box_config.get('box_overlay_ratio', 3200)
        text_scale = self.box_config.get('text_scale', 0.8) * box_overlay_ratio
        text_thickness = max(int(self.box_config.get('text_thickness', 2) * box_overlay_ratio), 1)
        text_padding = max(int(self.box_config.get('text_padding', 3) * box_overlay_ratio), 1)
        thickness = max(int(self.box_config.get('thickness', 3) * box_overlay_ratio), 1)

        # Set up colors based on annotation style
        if annotation_style == 'simple':
            colors = {
                'icon': {'box': (0, 255, 0), 'text': (0, 0, 0)},
                'text': {'box': (0, 0, 255), 'text': (255, 255, 255)}
            }
        else:  # colorful style
            palette = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255), (0,255,255)]

        annotated = image.copy()

        for idx, box_data in enumerate(boxes):
            bbox = box_data['bbox']
            box_type = box_data.get('box_type', 'unknown')
            content = box_data.get('content', '')

            # Get coordinates
            x1, y1 = int(bbox[0] * w), int(bbox[1] * h)
            x2, y2 = int(bbox[2] * w), int(bbox[3] * h)

            if annotation_style == 'simple':
                box_color = colors.get(box_type, {'box': (128, 128, 128)})['box']
                text_color = colors.get(box_type, {'text': (255, 255, 255)})['text']
            else:
                box_color = palette[idx % len(palette)]
                luminance = 0.299 * box_color[0] + 0.587 * box_color[1] + 0.114 * box_color[2]
                text_color = (0,0,0) if luminance > 160 else (255,255,255)

            # Draw bounding box
            cv2.rectangle(annotated, (x1, y1), (x2, y2), box_color, thickness)

            # Prepare label
            label = f"{box_type}"
            if content:
                # Truncate long text
                if len(content) > 30:
                    content = content[:27] + "..."
                label += f": {content}"

            # Get text size
            text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX,
                                      text_scale, text_thickness)[0]

            # Draw text background and text
            cv2.rectangle(annotated,
                        (x1, y1 - text_size[1] - 2 * text_padding),
                        (x1 + text_size[0] + 2 * text_padding, y1),
                        box_color, -1)

            cv2.putText(annotated, label,
                        (x1 + text_padding, y1 - text_padding),
                        cv2.FONT_HERSHEY_SIMPLEX, text_scale,
                        text_color, text_thickness, cv2.LINE_AA)

        print(f"Image annotation completed with {len(boxes)} elements.")
        return annotated

    def analyze(self, image_path: str, use_ocr: bool = False, 
                confidence_threshold: float = 0.05) -> Tuple[Image.Image, pd.DataFrame]:
        """
        Analyze an image with YOLO and optionally OCR.
        
        Args:
            image_path: Path to image file
            use_ocr: Whether to use OCR for text detection
            confidence_threshold: Confidence threshold for YOLO (default: 0.05)
            
        Returns:
            Tuple containing:
                - Annotated image as PIL Image
                - DataFrame with detection results
        """
        if not self._is_setup:
            raise RuntimeError("Please run setup() first")

        # Check if OCR is requested but not available
        if use_ocr and self.ocr_device is None:
            print("Warning: OCR was requested but OCR is disabled (ocr_device=None). No text detection will be performed.")
            use_ocr = False

        # Load and process image
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
            
        image = Image.open(image_path).convert("RGB")
        w, h = image.size
        boxes = []
        start = time.time()
        print(f"Image loaded ({w}x{h}). Timer started!")

        # YOLO detection
        yolo_start = time.time()
        yolo_results = self.yolo.predict(source=image, conf=confidence_threshold, iou=0.7)[0]
        yolo_boxes = yolo_results.boxes.xyxy.cpu().numpy()
        yolo_conf = yolo_results.boxes.conf.cpu().numpy()

        for idx, (box, conf) in enumerate(zip(yolo_boxes, yolo_conf)):
            boxes.append({
                'box_id': f'icon_{idx}',
                'box_type': 'icon',
                'content': None,
                'bbox': [box[0]/w, box[1]/h, box[2]/w, box[3]/h],
                'confidence': float(conf),
                'interactivity': True,
                'source': 'yolo'
            })
        print(f"YOLO detection completed in {round(time.time() - yolo_start, 2)} seconds")
        print(f"Found {len(yolo_boxes)} icons/UI elements")

        # OCR detection if requested
        if use_ocr:
            ocr_start = time.time()
            try:
                ocr_boxes = self._process_ocr(np.array(image), w, h)
                boxes.extend(ocr_boxes)
                print(f"OCR completed in {round(time.time() - ocr_start, 2)} seconds")
            except Exception as e:
                print(f"OCR processing failed: {e}")

        # Create DataFrame and annotate
        df = pd.DataFrame(boxes)
        if len(df) > 0:
            df['ID'] = range(len(df))
        else:
            print("Warning: No objects detected in the image")
            df = pd.DataFrame(columns=['ID', 'box_id', 'box_type', 'content', 'bbox', 'confidence', 'interactivity', 'source'])

        annot_start = time.time()
        annotated_image = self._annotate_image(np.array(image), boxes, w, h)
        annotated_image = Image.fromarray(annotated_image)
        print(f"Image annotation completed in {round(time.time() - annot_start, 2)} seconds")
        print(f"Total analysis time: {round(time.time() - start, 2)} seconds")
        print(f"Analysis complete: Found {len(boxes)} total elements in image")

        return annotated_image, df

    def save_annotated_image(self, annotated_image: Image.Image, output_path: str) -> str:
        """
        Save annotated image to file.
        
        Args:
            annotated_image: Annotated image as PIL Image
            output_path: Path to save the image
            
        Returns:
            Path to saved image
        """
        # Create directories if they don't exist
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        annotated_image.save(output_path)
        print(f"Annotated image saved to {output_path}")
        return output_path