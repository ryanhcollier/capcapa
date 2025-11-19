import os
import time
from datetime import datetime
import mss
from PIL import Image

# Global variable to control the screenshot loop
capturing = False

def create_storage_dir():
    """Create a directory on the desktop to store screenshots if it doesn't exist."""
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    storage_path = os.path.join(desktop, "Screenshots")
    if not os.path.exists(storage_path):
        os.makedirs(storage_path)
    return storage_path

def capture_screenshot(storage_path):
    """Capture the screen and save it to the specified path."""
    with mss.mss() as sct:
        # The screen part to capture. sct.monitors[0] is the full screen, sct.monitors[1] is the primary monitor.
        if len(sct.monitors) > 1:
            monitor = sct.monitors[1]
        else:
            monitor = sct.monitors[0]

        # Grab the data
        sct_img = sct.grab(monitor)

        # Create an Image
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

        # Generate filename
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"screenshot_{timestamp}.png"
        filepath = os.path.join(storage_path, filename)

        # Save to the picture file
        img.save(filepath)
        print(f"Screenshot saved to {filepath}")

import tkinter as tk
from functools import partial

# --- Main Application Logic ---

def start_capturing(start_button, stop_button, root, storage_path):
    """Starts the screenshot capturing loop."""
    global capturing
    capturing = True
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    capturing_loop(stop_button, root, storage_path)

def stop_capturing(start_button, stop_button):
    """Stops the screenshot capturing loop."""
    global capturing
    capturing = False
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

def capturing_loop(stop_button, root, storage_path):
    """The main loop for capturing screenshots every 5 seconds."""
    if capturing:
        capture_screenshot(storage_path)
        root.after(5000, lambda: capturing_loop(stop_button, root, storage_path))

if __name__ == "__main__":
    storage_directory = create_storage_dir()

    # Create the main application window
    app = tk.Tk()
    app.title("Capcapa")

    frame = tk.Frame(app, padx=10, pady=10)
    frame.pack(padx=10, pady=10)

    # Create the buttons
    start_btn = tk.Button(frame, text="Start")
    start_btn.pack(side=tk.LEFT, padx=5)

    stop_btn = tk.Button(frame, text="Stop", state=tk.DISABLED)
    stop_btn.pack(side=tk.LEFT, padx=5)

    # Assign commands with proper arguments
    start_btn.config(command=lambda: start_capturing(start_btn, stop_btn, app, storage_directory))
    stop_btn.config(command=lambda: stop_capturing(start_btn, stop_btn))

    app.mainloop()
