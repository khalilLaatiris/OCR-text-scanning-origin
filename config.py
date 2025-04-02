import os
import logging

class Config:
    """
    Configuration class storing image processing parameters, OCR engine settings, and format conversion rules.
    """
    def __init__(self):
        self.input_path = ".input"
        self.output_path = ".output"
        self.language = "eng"
        self.tesseract_path = os.getenv("TESSERACT")

        # Image processing parameters
        self.denoise_params = {
            'h': 10,
            'template_window_size': 7,
            'search_window_size': 21
        }
        self.clahe_params = {
            'clip_limit': 2.0,
            'tile_grid_size': (8, 8)
        }
        self.adaptive_thresh_params = {
            'block_size': 11,
            'c': 2
        }

        # OCR engine settings
        self.psm = 3  # Page segmentation mode
        self.oem = 1  # OCR Engine mode

        # Format conversion rules
        self.metadata = {
            'original_filename': None,
            'processing_timestamp': None,
            'confidence_scores': None
        }

        logger = logging.getLogger(__name__)
        logger.debug(f"Tesseract path: {self.tesseract_path}")