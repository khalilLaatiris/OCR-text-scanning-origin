import os
import pytesseract
import logging
from config import Config
class OCREngine:
    def __init__(self,config:Config):
        self.config = config
    
    def process_image(self,image):
        """
        Performs OCR on a processed image using Tesseract with error handling and version validation.
        """
        logger = logging.getLogger(__name__)
        try:
            # Configure Tesseract path
            pytesseract.tesseract_cmd = self.config.tesseract_path
            if not os.path.isfile(pytesseract.tesseract_cmd):
                raise FileNotFoundError(
                    f"Tesseract executable not found at: {pytesseract.tesseract_cmd}\n"
                    f"1. Install Tesseract from https://github.com/UB-Mannheim/tesseract/wiki\n"
                    f"2. Set TESSERACT_PATH in .env or system environment variables"
                )
            logger.info("OCR started")
            # # Verify Tesseract accessibility
            # tesseract_version = pytesseract.get_tesseract_version()
            # logger.debug(f"Tesseract version: {tesseract_version}")

            # Perform OCR with configured parameters
            return pytesseract.image_to_string(
                image,
                lang=self.config.language,
                config=f'--psm {self.config.psm} --oem {self.config.oem}'
            )

        except Exception as e:
            logger.error(f"Error during OCR processing: {e}")
            raise
