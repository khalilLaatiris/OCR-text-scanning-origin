import os
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import threading
import cv2
import logging

class UploadPanel:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.setup_ui()

    def setup_ui(self):
        # File upload panel
        self.upload_panel = ttk.Frame(self.frame)
        self.setup_upload_ui()
        self.upload_panel.pack(fill=tk.BOTH, expand=True)

        # Progress bar
        self.progress = ttk.Progressbar(self.frame, mode='determinate')
        self.progress.pack(fill=tk.X, pady=5)

        # Thumbnail canvas
        self.canvas = tk.Canvas(self.frame)
        self.scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.thumbnail_frame = ttk.Frame(self.canvas)
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas.create_window((0,0), window=self.thumbnail_frame, anchor=tk.NW)
        self.thumbnail_frame.bind("<Configure>", self.on_frame_configure)


    def setup_upload_ui(self):
        ttk.Label(self.upload_panel, text="File Upload", font=('Arial', 12, 'bold')).pack(pady=5)
        btn_frame = ttk.Frame(self.upload_panel)
        ttk.Button(btn_frame, text="Select Files", command=self.select_files).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear Selection", command=self.clear_files).pack(side=tk.RIGHT, padx=5)
        btn_frame.pack(fill=tk.X, pady=5)
        
        self.file_listbox = tk.Listbox(self.upload_panel, height=8)
        self.file_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def select_files(self):
        filetypes = (
            ('Image files', '*.png *.jpg *.jpeg *.tiff'),
            ('All files', '*.*')
        )
        filenames = filedialog.askopenfilenames(
            title='Select documents',
            filetypes=filetypes
        )
        for f in filenames:
            if self.validate_file(f):
                self.file_listbox.insert(tk.END, f)
                self.add_thumbnail(f)

    def validate_file(self, path):
        if os.path.getsize(path) > 10*1024*1024:  # 10MB limit
            logging.error("File too large")
            return False
        return path.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff'))

    def clear_files(self):
        self.file_listbox.delete(0, tk.END)
        for widget in self.thumbnail_frame.winfo_children():
            widget.destroy()

    def add_thumbnail(self, image_source):
        thumbnail = ttk.Frame(self.thumbnail_frame)
        thumbnail.pack(side=tk.TOP, padx=2, pady=2)
        if isinstance(image_source, str):  # File path
            img = Image.open(image_source)
        img.thumbnail((100, 100))
        photo = ImageTk.PhotoImage(img)
        
        label = ttk.Label(thumbnail, image=photo)
        label.image = photo
        label.pack(side=tk.LEFT)
        
        ttk.Label(thumbnail, text=os.path.basename(image_source)).pack(side=tk.LEFT)