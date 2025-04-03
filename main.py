import tkinter as tk
from tkinter import ttk, messagebox

import cv2
from upload_document import UploadPanel
from image_preprocess import ImagePreprocessor
from ocr_engine import OCREngine
from result_display import ResultDisplay
import threading
import queue
import logging
from config import Config

class OCRApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Document OCR Suite")
        self.root.state('zoomed')  # Maximize the window
        
        self.current_docs = []
        self.processed_images = []
        self.ocr_results = []
        self.setup_ui()
        self.setup_threading()
        
    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Upload panel
        self.upload_panel = UploadPanel(main_frame)
        self.upload_panel.frame.pack(fill=tk.BOTH, expand=True)
        
        # Control toolbar
        toolbar = ttk.Frame(main_frame)
        self.btn_preprocess = ttk.Button(toolbar, text="Preprocess", 
                                      command=self.start_preprocessing)
        self.btn_ocr = ttk.Button(toolbar, text="Run OCR", 
                                command=self.start_ocr, state=tk.DISABLED)
        self.btn_results = ttk.Button(toolbar, text="View Results", 
                                    command=self.show_results, state=tk.DISABLED)
        
        self.btn_preprocess.pack(side=tk.LEFT, padx=5)
        self.btn_ocr.pack(side=tk.LEFT, padx=5)
        self.btn_results.pack(side=tk.LEFT, padx=5)
        toolbar.pack(fill=tk.X, pady=5)
        
        # Status bar
        self.status = ttk.Label(main_frame, text="Ready", relief=tk.SUNKEN)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='determinate')
        self.progress.pack(fill=tk.X, pady=2)
        
    def setup_threading(self):
        self.ocr_thread = None
        self.preprocess_thread = None
        
    def start_preprocessing(self):
        if not self.upload_panel.file_listbox.get(0, tk.END):
            messagebox.showwarning("No Documents", "Please upload documents first")
            return
            
        self.preprocess_thread = threading.Thread(target=self.run_preprocessing)
        self.preprocess_thread.start()
        self.root.after(100, self.check_preprocess)
        
    def run_preprocessing(self):
        self.progress["value"] = 0
        total = len(self.upload_panel.file_listbox.get(0, tk.END))
        
        for idx, path in enumerate(self.upload_panel.file_listbox.get(0, tk.END)):
            try:
                preprocessor = ImagePreprocessor(self.root, path)
                self.processed_images.append(preprocessor)
                # cv2.imwrite(f"processed_{idx}.png", preprocessor.current_image)
                self.progress["value"] = (idx+1)/total * 100
            except Exception as e:
                logging.error(f"Preprocessing failed: {e}")
                
        self.btn_ocr["state"] = tk.NORMAL
        self.status["text"] = "Preprocessing complete"
        
    def check_preprocess(self):
        if self.preprocess_thread.is_alive():
            self.root.after(100, self.check_preprocess)
        else:
            self.progress["value"] = 0
            
    def start_ocr(self):
        self.ocr_thread = threading.Thread(target=self.run_ocr)
        self.ocr_thread.start()
        self.root.after(100, self.check_ocr)
        self.btn_results["state"] = tk.DISABLED
        
    def run_ocr(self):
       
        self.progress["value"] = 0
        total = len(self.processed_images)
        import argparse
        ocr_engine = OCREngine(Config())
        
        
        for idx, img_processor in enumerate(self.processed_images):
            try:
                result = ocr_engine.process_image(cv2.cvtColor(img_processor.current_image,cv2.COLOR_RGB2GRAY))
                self.ocr_results.append(
                    {
                        "input_file": img_processor.image_path,
                        "process_image" : img_processor.current_image,
                        "text": result,
                    })
                self.progress["value"] = (idx+1)/total * 100
            except Exception as e:
                logging.error(f"OCR failed: {e}")
                                
        self.btn_results["state"] = tk.NORMAL
        self.status["text"] = "OCR processing complete"
        
    def check_ocr(self):
        if self.ocr_thread.is_alive():
            self.root.after(100, self.check_ocr)
        else:
            self.progress["value"] = 0
            
    def show_results(self):
        for image_processor in self.ocr_results:
            img_path = image_processor["input_file"]
            text = image_processor["text"]
            ResultDisplay(self.root, img_path, text)
            
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    logger = logging.getLogger('simple_example')
    # create file handler that logs debug and higher level messages
    fh = logging.FileHandler('main.log')
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    # add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)
    app = OCRApplication()
    app.run()