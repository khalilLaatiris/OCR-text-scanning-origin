# OCR Pipeline

This project is an OCR (Optical Character Recognition) pipeline designed to process images and extract text from them. The pipeline includes modules for image preprocessing, OCR processing, result display, and document uploading.

## Installation

To set up the project, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/khalilLaatiris/OCR-text-scanning-origin.git
   ```

2. Set up a virtual environment (optional but recommended):
   ```bash
   sh setup_env.sh  # On Windows, use `setup_env.bat`
   ```

3. Make sure that Tesseract OCR is installed on your system. For installation instructions, refer to the [Tesseract OCR GitHub page](https://github.com/tesseract-ocr/tesseract).

## Usage

To run the main script, use the following command:
```bash
python main.py
```

### Configuration

The `config.py` file contains configuration settings for the OCR pipeline. Make sure to set the appropriate environment variables if needed (e.g., Tesseract path).

### Main Modules

- `image_preprocess.py`: Handles image preprocessing tasks such as noise reduction, binarization, and other image enhancements.
- `ocr_engine.py`: Contains the main OCR processing logic using `pytesseract`.
- `result_display.py`: Displays the OCR results in a user-friendly format.
- `upload_document.py`: Handles the uploading of documents for OCR processing.

## Dependencies

The project requires the following Python packages (see `requirements.txt` for specific versions):
- pytesseract
- opencv-python
- scikit-image
- numpy
- pandas
- python-dotenv
- pywavelets
- Pillow
- scipy

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.
you want to descuss ? see (my portfolio)[..\khalillaatiris]

## License

This project is licensed under the MIT License - see the LICENSE file for details.
