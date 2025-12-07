import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import rawpy
import os
from pathlib import Path
import datetime
import subprocess
import platform


# -----------------------------------------
# Output directory (~/Downloads/getpng)
# -----------------------------------------
OUTPUT_DIR = Path.home() / "Downloads/getpng"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def open_output_folder():
    """Open the output directory in the system file manager."""
    path = str(OUTPUT_DIR)
    if platform.system() == "Windows":
        subprocess.Popen(f'explorer "{path}"')
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


def convert_image(input_path):
    """
    Convert a single image (RAW or normal) to PNG in OUTPUT_DIR.
    Returns (True, output_path) on success, or (False, error_message) on failure.
    """
    filename = os.path.basename(input_path)
    output_path = OUTPUT_DIR / (Path(filename).stem + ".png")

    # Try rawpy first (for RAW / DNG)
    try:
        with rawpy.imread(input_path) as raw:
            rgb = raw.postprocess()
        img = Image.fromarray(rgb)
        img.save(output_path, "PNG")
        return True, str(output_path)

    except Exception:
        # Fallback to Pillow (for normal images or unsupported RAW)
        try:
            img = Image.open(input_path)
            img.save(output_path, "PNG")
            return True, str(output_path)
        except Exception as e:
            return False, str(e)


def choose_files():
    """Open file dialog and let user select multiple images."""
    global selected_files

    file_paths = filedialog.askopenfilenames(
        title="Select images",
        filetypes=[
            ("Images", "*.jpg *.jpeg *.png *.bmp *.tif"),
            ("RAW", "*.dng *.nef *.cr2 *.arw *.raf *.rw2"),
            ("All files", "*.*"),
        ],
    )

    if not file_paths:
        return

    selected_files = list(file_paths)
    total = len(selected_files)

    file_count_label.configure(text=f"Selected {total} file(s)")

    # Clear previous thumbnails
    for widget in thumb_frame.winfo_children():
        widget.destroy()

    # Show thumbnails for selected images
    for p in selected_files:
        try:
            img = Image.open(p)
            img.thumbnail((80, 80))
            tk_img = ImageTk.PhotoImage(img)

            lbl = ctk.CTkLabel(thumb_frame, image=tk_img, text="")
            lbl.image = tk_img
            lbl.pack(side="left", padx=5)
        except Exception:
            # If thumbnail fails, just skip that file
            pass

    # Reset progress area
    progress_label.configure(text="Ready to convert.")
    progress_bar.set(0)
    status_label.configure(text="")
    convert_button.configure(state="normal")
    open_folder_button.configure(state="disabled")

    # Clear converted preview
    for widget in result_frame.winfo_children():
        widget.destroy()


def convert_files():
    """Convert all selected files with progress text + progress bar."""
    if not selected_files:
        return

    total = len(selected_files)
    success = 0

    # Clear previous converted thumbnails
    for widget in result_frame.winfo_children():
        widget.destroy()

    convert_button.configure(state="disabled")
    progress_bar.set(0)
    progress_label.configure(text=f"Converting 0 / {total}...")
    status_label.configure(text="Converting...")

    root.update_idletasks()

    for idx, file_path in enumerate(selected_files, start=1):
        ok, _ = convert_image(file_path)
        if ok:
            success += 1

            # Add a thumbnail for converted file
            try:
                img = Image.open(file_path)
                img.thumbnail((80, 80))
                tk_img = ImageTk.PhotoImage(img)
                lbl = ctk.CTkLabel(result_frame, image=tk_img, text="")
                lbl.image = tk_img
                lbl.pack(side="left", padx=5)
            except Exception:
                pass

        # Update progress text + bar
        progress_label.configure(text=f"Converting {idx} / {total}...")
        progress_bar.set(idx / total)
        root.update_idletasks()

    # Final status message
    if success > 0:
        status_label.configure(
            text=f"Done. Converted {success} of {total} file(s) → {OUTPUT_DIR}"
        )
        open_folder_button.configure(state="normal")
    else:
        status_label.configure(text="Conversion failed for all files.")

    convert_button.configure(state="normal")


def update_datetime():
    """Update date + time display (no seconds)."""
    now = datetime.datetime.now()
    # Example: Tuesday, Nov 25 2025 — 09:31 AM
    text = now.strftime("%A, %b %d %Y — %I:%M %p")
    datetime_label.configure(text=text)
    root.after(1000, update_datetime)


# -----------------------------------------
# UI SETUP (CustomTkinter)
# -----------------------------------------
ctk.set_appearance_mode("dark")  # "dark" or "light"
ctk.set_default_color_theme("blue")  # accent color theme

root = ctk.CTk()
root.title("Modern Image / RAW to PNG Converter")
root.geometry("860x640")

selected_files = []

# Title
title_label = ctk.CTkLabel(
    root,
    text="Image to PNG Converter",
    font=("Arial", 28, "bold"),
)
title_label.pack(pady=(20, 5))

# Date + time (no seconds)
datetime_label = ctk.CTkLabel(root, text="", font=("Arial", 14))
datetime_label.pack(pady=(0, 15))
update_datetime()

# Choose files button
choose_button = ctk.CTkButton(
    root,
    text="Choose Files",
    command=choose_files,
    width=230,
    height=40,
    corner_radius=12,
    font=("Arial", 16),
)
choose_button.pack(pady=5)

file_count_label = ctk.CTkLabel(root, text="No files selected", font=("Arial", 14))
file_count_label.pack(pady=5)

# Selected thumbnails
thumb_frame_label = ctk.CTkLabel(
    root, text="Selected files preview:", font=("Arial", 13)
)
thumb_frame_label.pack(pady=(15, 0))

thumb_frame = ctk.CTkFrame(root, height=110)
thumb_frame.pack(pady=5, padx=10, fill="x")

# Convert button
convert_button = ctk.CTkButton(
    root,
    text="Convert to PNG",
    command=convert_files,
    width=230,
    height=40,
    corner_radius=12,
    font=("Arial", 16),
    state="disabled",
)
convert_button.pack(pady=15)

# Progress text + bar
progress_label = ctk.CTkLabel(root, text="", font=("Arial", 13))
progress_label.pack(pady=(5, 2))

progress_bar = ctk.CTkProgressBar(root, width=400)
progress_bar.set(0)
progress_bar.pack(pady=(0, 10))

# Converted thumbnails
result_frame_label = ctk.CTkLabel(
    root, text="Converted files preview:", font=("Arial", 13)
)
result_frame_label.pack(pady=(10, 0))

result_frame = ctk.CTkFrame(root, height=110)
result_frame.pack(pady=5, padx=10, fill="x")

# Status text
status_label = ctk.CTkLabel(root, text="", font=("Arial", 13))
status_label.pack(pady=10)

# Open output folder button
open_folder_button = ctk.CTkButton(
    root,
    text="Open Output Folder",
    command=open_output_folder,
    width=230,
    height=40,
    corner_radius=12,
    font=("Arial", 16),
    state="disabled",
)
open_folder_button.pack(pady=15)

root.mainloop()
