import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import io
from rembg import remove

class BackgroundRemoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Background Remover App")

        # Initialize variables
        self.image_path = None
        self.original_image = None
        self.processed_image = None

        # Create widgets
        self.canvas = tk.Canvas(self.root, width=600, height=400)
        self.canvas.pack()

        self.select_button = tk.Button(self.root, text="Select Image", command=self.select_image)
        self.select_button.pack(side=tk.TOP, padx=10, pady=10)

        self.remove_button = tk.Button(self.root, text="Remove Background", command=self.remove_background)
        self.remove_button.pack(side=tk.TOP, padx=10, pady=10)

        self.save_button = tk.Button(self.root, text="Save Image", command=self.save_image)
        self.save_button.pack(side=tk.TOP, padx=10, pady=10)

    def select_image(self):
        self.image_path = filedialog.askopenfilename()
        if self.image_path:
            self.load_image()

    def load_image(self):
        self.original_image = Image.open(self.image_path)
        self.processed_image = self.original_image.copy()
        self.display_image(self.original_image)

    def display_image(self, image):
        tk_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
        self.canvas.image = tk_image

    def remove_background(self):
        if self.image_path:
            # Load image using rembg and get bytes
            with open(self.image_path, "rb") as f:
                img_bytes = f.read()

            # Remove background using rembg
            img_bytes = remove(img_bytes)

            # Convert bytes back to Image
            img = Image.open(io.BytesIO(img_bytes))

            # Display processed image
            self.processed_image = img.convert("RGBA")
            self.display_image(self.processed_image)

    def save_image(self):
        if self.processed_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            if file_path:
                # Save the image
                self.processed_image.save(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = BackgroundRemoverApp(root)
    root.mainloop()
