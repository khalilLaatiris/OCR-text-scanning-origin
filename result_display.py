import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import pytesseract
import cv2
import os

class ResultDisplay:
    def __init__(self, parent, image_path, ocr_text):
        self.root = tk.Toplevel(parent)
        self.root.title("OCR Results")
        self.root.state("zoomed")
        
        self.image_path = image_path
        self.original_text = ocr_text
        self.current_text = ocr_text
        self.highlight_tag = None
        
        self.setup_ui()
        self.load_image()
        self.setup_text_editor()
        
    def setup_ui(self):
        # Split panel
        self.paned_window = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # Image panel
        self.image_frame = ttk.Frame(self.paned_window)
        self.image_label = ttk.Label(self.image_frame)
        self.image_label.pack(fill=tk.BOTH, expand=True)
        self.paned_window.add(self.image_frame, weight=1)

        # Text panel
        self.text_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(self.text_frame, weight=1)

        # Toolbar
        toolbar = ttk.Frame(self.root)
        toolbar.pack(fill=tk.X)
        ttk.Button(toolbar, text="Save Text", command=self.save_text).pack(side=tk.LEFT)
        ttk.Button(toolbar, text="Export PDF", command=self.export_pdf).pack(side=tk.LEFT)
        ttk.Button(toolbar, text="Copy", command=self.copy_text).pack(side=tk.RIGHT)

    def load_image(self):
        image = cv2.imread(self.image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(image)
        img.thumbnail((800, 600))
        self.tk_image = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.tk_image)

    def setup_text_editor(self):
        # Text widget with scrollbar
        self.text_scroll = ttk.Scrollbar(self.text_frame)
        self.text_editor = tk.Text(self.text_frame, wrap=tk.WORD, yscrollcommand=self.text_scroll.set)
        self.text_scroll.config(command=self.text_editor.yview)
        
        self.text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_editor.pack(fill=tk.BOTH, expand=True)
        
        self.text_editor.insert(tk.END, self.current_text)
        self.text_editor.bind("<KeyRelease>", self.update_text)
        
        # Setup text highlighting
        self.text_editor.tag_config("highlight", background="yellow")

    def update_text(self, event):
        self.current_text = self.text_editor.get("1.0", tk.END)
        
    def save_text(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if path:
            with open(path, 'w') as f:
                f.write(self.current_text)

    def export_pdf(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if path:
            # Would need reportlab or similar PDF library installed
            pass
            
    def copy_text(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.current_text)

    def sync_highlight(self, line_num):
        # Clear previous highlight
        if self.highlight_tag:
            self.text_editor.tag_remove("highlight", self.highlight_tag[0], self.highlight_tag[1])
            
        # Calculate text position
        start = f"{line_num}.0"
        end = f"{line_num + 1}.0"
        self.text_editor.tag_add("highlight", start, end)
        self.highlight_tag = (start, end)
        self.text_editor.see(start)