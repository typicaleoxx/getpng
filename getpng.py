import tkinter as tk
from tkinter import filedialog, messagebox
import os
from PIL import Image
import rawpy
import datetime
import subprocess
import platform
from pathlib import Path


# Output directory: ~/Downloads/getpng/
OUTPUT_DIR = Path.home() / "Downloads/getpng"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def open_output_folder():
    """Open the output directory."""
    path = str(OUTPUT_DIR)

    if platform.system() == "Windows":
        subprocess.Popen(f'explorer "{path}"')
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


def convert_image(input_path):
    """Convert any image (RAW or regular) to PNG."""
    filename = os.path.basename(input_path)
    filename_no_ext = os.path.splitext(filename)[0]
    output_path = OUTPUT_DIR / f"{filename_no_ext}.png"

    # Try RAW first
    try:
        with rawpy.imread(input_path) as raw:
            rgb = raw.postprocess()
        img = Image.fromarray(rgb)
        img.save(output_path, "PNG")
        return True, str(output_path)

    except Exception:
        # Fallback to Pillow
        try:
            img = Image.open(input_path)
            img.save(output_path, "PNG")
            return True, str(output_path)
        except Exception as e:
            return False, str(e)


def choose_files():
    global selected_files

    selected_files = filedialog.askopenfilenames(
        title="Select images (multiple allowed)",
        filetypes=[
            ("Images", "*.jpg *.jpeg *.png *.bmp *.tif"),
            ("RAW formats", "*.dng *.nef *.cr2 *.arw *.raf *.rw2"),
            ("All files", "*.*"),
        ],
    )

    if selected_files:
        file_label.config(text=f"Selected {len(selected_files)} files")
        convert_button.config(state="normal")
        status_label.config(text="")
        download_button.config(state="disabled")


def convert_files():
    if not selected_files:
        return

    status_label.config(text="Converting...")
    root.update_idletasks()

    success = 0

    for f in selected_files:
        ok, msg = convert_image(f)
        if ok:
            success += 1

    if success > 0:
        status_label.config(text=f"Converted {success} file(s). Saved in: {OUTPUT_DIR}")
        download_button.config(state="normal")
    else:
        status_label.config(text="Conversion failed for all files.")
        messagebox.showerror("Error", "No files were converted.")


def update_clock():
    now = datetime.datetime.now().strftime("%I:%M:%S %p")
    clock_label.config(text=f"Current Time: {now}")
    root.after(1000, update_clock)


# ------------- UI -------------

root = tk.Tk()
root.title("Image / RAW to PNG Converter")
root.geometry("700x450")
root.configure(bg="#1f1f1f")

selected_files = []

title_label = tk.Label(
    root,
    text="Image to PNG Converter",
    font=("Arial", 22, "bold"),
    bg="#1f1f1f",
    fg="white",
)
title_label.pack(pady=20)

clock_label = tk.Label(root, text="", font=("Arial", 12), bg="#1f1f1f", fg="white")
clock_label.pack(pady=5)

choose_button = tk.Button(
    root, text="Choose Files", font=("Arial", 14), width=20, command=choose_files
)
choose_button.pack(pady=10)

file_label = tk.Label(
    root, text="No files selected", font=("Arial", 12), bg="#1f1f1f", fg="#cccccc"
)
file_label.pack(pady=5)

convert_button = tk.Button(
    root,
    text="Convert",
    font=("Arial", 14),
    width=20,
    state="disabled",
    command=convert_files,
)
convert_button.pack(pady=15)

status_label = tk.Label(
    root, text="", font=("Arial", 12), bg="#1f1f1f", fg="lightgreen"
)
status_label.pack(pady=5)

download_button = tk.Button(
    root,
    text="Open Output Folder",
    font=("Arial", 14),
    width=22,
    state="disabled",
    command=open_output_folder,
)
download_button.pack(pady=15)

update_clock()

root.mainloop()
