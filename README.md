Image to PNG Converter

A simple Python application that converts images, including RAW formats such as DNG, NEF, CR2, and ARW, into PNG files.
This tool provides a small graphical interface built with Tkinter and works on Windows, macOS, and Linux.

Features

Converts standard image formats (JPG, JPEG, BMP, TIFF, PNG).

Converts RAW camera formats (DNG, NEF, CR2, ARW, RAF, RW2).

Simple and clean Tkinter user interface.

Output PNG is saved in the same directory as the input file.

Requires only two Python libraries: Pillow and rawpy.

Requirements

Make sure you have Python 3.8 or newer installed.
Tkinter comes with Python by default.

Install the required dependencies:

pip install pillow rawpy

If you encounter issues related to array handling, install NumPy as well:

pip install numpy

How to Run

Save the script into a file named, for example, image_to_png.py.

Open a terminal or command prompt in the same directory.

Run the script:

python image_to_png.py

When the window opens, click the “Choose File” button.

Select any supported image or RAW file.

The program will create a PNG version of your image in the same folder.

Supported Formats

Standard image formats:

JPG, JPEG

PNG

BMP

TIFF

RAW and camera formats:

DNG

NEF

CR2

ARW

RAF

RW2

Notes

The program saves the output PNG file using the same filename as the original, only the extension changes.

Some RAW files may process more slowly due to their size and complexity.

If a file cannot be opened or converted, an error message will be displayed.
