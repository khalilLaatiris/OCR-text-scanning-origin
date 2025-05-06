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

3. Install GUI dependencies:
   ```bash
   python3 -m pip install tk
   ```

4. Ensure Tesseract OCR is installed on your system. For installation instructions, refer to the [Tesseract OCR GitHub page](https://github.com/tesseract-ocr/tesseract).

## Usage

1. Launch the application:
   ```bash
   python main.py
   ```

2. GUI Workflow:
   1. Select image using "Upload Document" button
   2. Adjust processing parameters if needed
   3. Click "Process Image" to start OCR
   4. View results in the text display area
   5. Use "Clear All" to reset or "Export" to save results

![GUI Preview](docs/gui_preview.png)

### Key Features
- Asynchronous processing with progress updates
- Dark/Light mode toggle
- Input validation with immediate feedback
- Error handling with user-friendly messages

## Configuration

The `config.py` file contains configuration settings for the OCR pipeline. Make sure to set the appropriate environment variables if needed (e.g., Tesseract path).

## Main Modules

### OCRApplication Class Structure
The core GUI application built with Tkinter implements the Model-View-Controller pattern:

```python
class OCRApplication:
    def __init__(self, root: Tk)  # Initializes main window and components
    def create_widgets(self)       # Constructs UI layout
    def init_upload_panel(self)    # Configures file upload section
    def init_control_buttons(self) # Sets up action buttons
    def init_status_bar(self)      # Creates progress/status indicators
    def process_image(self)        # Manages OCR processing pipeline
    def toggle_dark_mode(self)     # Handles theme switching
    def validate_inputs(self)      # Performs pre-processing checks
    def thread_safe_update(self, func, *args)  # Ensures GUI thread safety
```

### GUI Component Breakdown

#### Upload Panel
- File selection dialog supporting common image formats (PNG, JPG, BMP)
- Preview thumbnail generation
- Drag-and-drop functionality
- File size and type validation

#### Control Buttons
1. **Process Image**:
   - Initiates OCR pipeline
   - Disables during processing to prevent duplicate requests
   - Shows animated loading state

2. **Toggle Dark Mode**:
   - Switches between light/dark themes
   - Persists preference across sessions

3. **Clear All**:
   - Resets input fields
   - Clears preview images and text results
   - Resets status indicators

#### Status Bars
- Real-time processing stages:
  1. File upload validation
  2. Image preprocessing
  3. OCR extraction
  4. Post-processing
- Error message display with auto-clear timer
- Progress percentage indicator

### Workflow Sequence
1. User selects image file through Upload Panel
2. Application validates file format and size
3. Validated image passes to preprocessing module
4. OCR engine processes image using worker thread
5. Results are parsed and formatted for display
6. Final text output appears in scrollable text area
7. User can export results or restart process

### Threading Architecture
- **Main Thread**:
  - Handles all GUI updates and user interactions
  - Manages UI state changes
  - Uses `thread_safe_update` wrapper for cross-thread operations

- **Worker Thread**:
  ```python
  threading.Thread(target=self.process_image).start()
  ```
  - Executes CPU-intensive OCR operations
  - Communicates progress through queue system
  - Implements timeout safeguards

### Error Handling Mechanisms
1. **Input Validation**:
   - File type whitelisting (.png, .jpg, .bmp)
   - Maximum file size enforcement (10MB)
   - Empty field checks

2. **Exception Handling**:
   - Try/except blocks around OCR operations
   - Network error handling for external dependencies
   - Memory overflow protection for large files

3. **User Feedback**:
   - Color-coded status messages
   - Detailed error logs in main.log
   - Graceful degradation on failure

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
Want to discuss? See my portfolio [khalillaatiris](https://khalillaatiris.github.io/)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
