import os
import cv2
import numpy as np
import logging
import threading
import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from config import Config

class ImagePreprocessor:
    def __init__(self, parent, image_path):
        self.root = Toplevel(parent)
        self.root.title("Image Preprocessing")
        
        self.image_path = image_path
        self.original_image = cv2.imread(image_path)
        if self.original_image is None:
            raise FileNotFoundError(f"Could not load image at path: {image_path}")
        self.current_image = self.original_image.copy()
        self.edit_stack = []
        self.redo_stack = []
        
        self.setup_ui()
        self.show_image()
        
    def setup_ui(self):
        # Main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=BOTH, expand=True)
        
        # Image display
        self.image_panel = tk.Canvas(self.main_frame)
        self.image_panel.pack(side=LEFT, fill=BOTH, expand=True)
        
        # Toolbar
        toolbar = ttk.Frame(self.main_frame)
        toolbar.pack(side=RIGHT, fill=Y, padx=5, pady=5)
        
        # Processing buttons
        ttk.Button(toolbar, text="Rotate", command=self.rotate_dialog).pack(pady=2, fill=X)
        ttk.Button(toolbar, text="Crop", command=self.start_crop).pack(pady=2, fill=X)
        ttk.Button(toolbar, text="Contrast", command=self.contrast_dialog).pack(pady=2, fill=X)
        ttk.Button(toolbar, text="Binarize", command=self.binarize_image).pack(pady=2, fill=X)
        ttk.Button(toolbar, text="Deskew", command=self.deskew_image).pack(pady=2, fill=X)
        ttk.Button(toolbar, text="Undo", command=self.undo_edit).pack(pady=2, fill=X)
        ttk.Button(toolbar, text="Redo", command=self.redo_edit).pack(pady=2, fill=X)
        
        # Apply/Cancel buttons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(side=BOTTOM, fill=X, padx=5, pady=5)

        apply_button = ttk.Button(button_frame, text="Apply", command=self.apply_changes)
        apply_button.pack(side=RIGHT, padx=5)

        cancel_button = ttk.Button(button_frame, text="Cancel", command=self.cancel_changes)
        cancel_button.pack(side=RIGHT, padx=5)

        # Status bar
        self.status = ttk.Label(self.root, text="Ready", relief=SUNKEN)
        self.status.pack(side=BOTTOM, fill=X)
        
    def show_image(self):
        thread = threading.Thread(target=self._update_image_display)
        thread.start()
        
    def _update_image_display(self):
        image = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image.thumbnail((800, 600))
        photo = ImageTk.PhotoImage(image)
        self.image_panel.image = photo # keep a reference!
        self.image_panel.create_image(0, 0, image=photo, anchor=tk.NW)
        
    def rotate_dialog(self):
        dialog = Toplevel(self.root)
        dialog.title("Rotate Image")

        angle_label = ttk.Label(dialog, text="Enter rotation angle:")
        angle_label.pack(pady=5)

        angle_entry = ttk.Entry(dialog)
        angle_entry.pack(padx=10, pady=5)

        def apply_rotation():
            try:
                angle = float(angle_entry.get())
                self.apply_rotate(angle)
                dialog.destroy()  # Close the dialog after applying
            except ValueError:
                messagebox.showerror("Error", "Invalid angle. Please enter a number.")

        apply_button = ttk.Button(dialog, text="Apply", command=apply_rotation)
        apply_button.pack(pady=5)
    def apply_rotate(self, angle):
        self.edit_stack.append(self.current_image.copy())
        self.redo_stack.clear()
        
        (h, w) = self.current_image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        self.current_image = cv2.warpAffine(self.current_image, M, (w, h))
        self.show_image()
        
    def start_crop(self):
        self.crop_start = None
        self.crop_rect = None
        self.image_panel.bind("<Button-1>", self.crop_press)
        self.image_panel.bind("<B1-Motion>", self.crop_drag)
        self.image_panel.bind("<ButtonRelease-1>", self.crop_release)
        self.status.config(text="Select area to crop")
        
    def crop_press(self, event):
        self.crop_start = (event.x, event.y)
        
    def crop_drag(self, event):
        if self.crop_rect:
            self.image_panel.delete(self.crop_rect)
        x1, y1 = self.crop_start
        x2, y2 = event.x, event.y
        self.crop_rect = self.image_panel.create_rectangle(x1, y1, x2, y2, outline='red')
        
    def crop_release(self, event):
        x1, y1 = self.crop_start
        x2, y2 = event.x, event.y
        self.image_panel.delete(self.crop_rect)
        
        # Convert screen coordinates to image coordinates
        img_width = self.image_panel.winfo_width()
        img_height = self.image_panel.winfo_height()
        h, w = self.current_image.shape[:2]
        
        x1 = int((x1 / img_width) * w)
        x2 = int((x2 / img_width) * w)
        y1 = int((y1 / img_height) * h)
        y2 = int((y2 / img_height) * h)
        
        self.edit_stack.append(self.current_image.copy())
        self.redo_stack.clear()
        self.current_image = self.current_image[min(y1,y2):max(y1,y2), min(x1,x2):max(x1,x2)]
        self.show_image()
        self.status.config(text="Ready")
        
    def contrast_dialog(self):
        dialog = Toplevel(self.root)
        dialog.title("Adjust Contrast")
        
        alpha = DoubleVar(value=1.0)
        ttk.Scale(dialog, from_=0.1, to=3.0, variable=alpha).pack(padx=10, pady=5)
        ttk.Button(dialog, text="Apply",
                 command=lambda: self.apply_contrast(alpha.get())).pack(pady=5)
        
    def apply_contrast(self, alpha):
        self.edit_stack.append(self.current_image.copy())
        self.redo_stack.clear()
        self.current_image = cv2.convertScaleAbs(self.current_image, alpha=alpha, beta=0)
        self.show_image()
        
    def binarize_image(self):
        self.edit_stack.append(self.current_image.copy())
        self.redo_stack.clear()
        gray = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
        _, self.current_image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        self.current_image = cv2.cvtColor(self.current_image, cv2.COLOR_GRAY2BGR)
        self.show_image()
        
    def deskew_image(self):
        self.edit_stack.append(self.current_image.copy())
        self.redo_stack.clear()
        self.current_image = self._deskew(self.current_image)
        self.show_image()
        
    def _deskew(self, image):
        # Existing deskew implementation from original code
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150, apertureSize=3)
        kernel = np.ones((3,3), np.uint8)
        edges = cv2.dilate(edges, kernel, iterations=1)
        
        lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180,
                              threshold=100, minLineLength=gray.shape[1]//2,
                              maxLineGap=20)
        
        if lines is not None:
            angles = [np.arctan2(y2-y1, x2-x1)*180/np.pi for line in lines for x1,y1,x2,y2 in line]
            median_angle = np.median(angles)
            (h, w) = image.shape[:2]
            center = (w//2, h//2)
            M = cv2.getRotationMatrix2D(center, median_angle, 1.0)
            return cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC,
                                borderMode=cv2.BORDER_REPLICATE)
        return image
        
    def undo_edit(self):
        if self.edit_stack:
            self.redo_stack.append(self.current_image)
            self.current_image = self.edit_stack.pop()
            self.show_image()
            
    def redo_edit(self):
        if self.redo_stack:
            self.edit_stack.append(self.current_image)
            self.current_image = self.redo_stack.pop()
            self.show_image()

    def apply_changes(self):
        # Implement logic to apply all changes made in the preprocessor
        self.root.destroy()

    def cancel_changes(self):
        # Implement logic to discard all changes and close the preprocessor
        self.current_image = self.original_image.copy()
        self.root.destroy()

def preprocess_image(image_path: str, preprocess_flag: bool, config: Config):
    # Existing preprocessing logic (now uses the GUI class)
    root = Tk()
    root.withdraw()  # Hide the main Tkinter window
    preprocessor = ImagePreprocessor(root, image_path)
    preprocessor.root.wait_window()  # Wait until the preprocessor window is closed
    return preprocessor.current_image