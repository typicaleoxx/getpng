import tkinter as tk
from tkinter import filedialog, messagebox
import os
from PIL import Image
import rawpy


def convert_to_png(input_path):
    """
    Convert any supported image to PNG.
    RAW/DNG files use rawpy, normal formats use Pillow.
    """

    output_path = os.path.splitext(input_path)[0] + ".png"
    ext = os.path.splitext(input_path)[1].lower()

    try:
        # Handle RAW formats (DNG, NEF, CR2, ARW, etc.)
        if ext in [".dng", ".nef", ".cr2", ".arw", ".raf", ".rw2"]:
            with rawpy.imread(input_path) as raw:
                rgb = raw.postprocess()  # Convert RAW → RGB
            img = Image.fromarray(rgb)

        else:
            # Handle normal images via Pillow (JPG, PNG, TIFF…)
            img = Image.open(input_path)

        img.save(output_path, "PNG")
        return output_path

    except Exception as e:
        messagebox.showerror("Conversion Error", f"Failed to convert file:\n{e}")
        return None


def choose_file():
    """Open file dialog → convert file → show result message."""

    filepath = filedialog.askopenfilename(
        title="Select a file to convert to PNG",
        filetypes=[
            (
                "All supported",
                "*.dng *.nef *.cr2 *.arw *.raf *.rw2 *.jpg *.jpeg *.png *.bmp *.tif",
            ),
            ("RAW files", "*.dng *.nef *.cr2 *.arw *.raf *.rw2"),
            ("Images", "*.jpg *.jpeg *.png *.bmp *.tif"),
        ],
    )

    if filepath:
        result = convert_to_png(filepath)
        if result:
            messagebox.showinfo("Success", f"PNG saved at:\n{result}")


# ---------------------------
# Tkinter UI Setup
# ---------------------------

root = tk.Tk()
root.title("Image → PNG Converter")
root.geometry("420x180")

label = tk.Label(
    root, text="Convert any image (including DNG/RAW) to PNG", font=("Arial", 12)
)
label.pack(pady=20)

btn = tk.Button(
    root, text="Choose File", command=choose_file, font=("Arial", 12), width=20
)
btn.pack()

root.mainloop()
