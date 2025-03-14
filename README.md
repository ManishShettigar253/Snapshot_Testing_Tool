# Snapshot Testing Tool

A simple web application that compares two images (UI of 2 different versions of s/w ) and provides a quantitative analysis of their differences.

## Features

- Upload and compare two images
- Calculate the percentage difference between images
- Automatic image resizing when dimensions differ
- User-friendly web interface

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python tool.py
   ```
4. Open your browser and navigate to `http://127.0.0.1:5001`

## Usage

1. Upload two images using the web interface
2. Click "Test"
3. View the comparison result showing the percentage difference between the images



## Technical Details

- Built with Flask web framework
- Uses OpenCV for image processing
- CORS enabled for cross-origin requests
- Secure file handling with UUID-based filenames
