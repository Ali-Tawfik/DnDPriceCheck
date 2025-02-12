import cv2
import sys
import os
import numpy as np
from paddleocr import PaddleOCR
from mss import mss
import keyboard
import matplotlib.pyplot as plt
import re
import tkinter as tk
from multiprocessing import Queue, Process
import time

# Add the script's directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import other modules
#smart_match,attribute_to_acrynom

from checker_overlay import start_overlay,show_text
from dnd_process import check_secondary_prices
# Constants
SCREENSHOTS_DIR = './screenshots'

# Ensure the screenshots directory exists
if not os.path.exists(SCREENSHOTS_DIR):
    os.makedirs(SCREENSHOTS_DIR)

# Initialize PaddleOCR and MSS
ocr = PaddleOCR()
sct = mss()


PLT_EN = False


def get_next_screenshot_number():
    """Get the next available screenshot number based on existing files in the directory."""
    existing_files = os.listdir(SCREENSHOTS_DIR)
    screenshot_numbers = []

    for file in existing_files:
        if file.startswith('item_') and file.endswith('.png'):
            try:
                num = int(file.split('_')[1].split('.')[0])
                screenshot_numbers.append(num)
            except (IndexError, ValueError):
                continue

    if not screenshot_numbers:
        return 0
    return max(screenshot_numbers) + 1

def save_screenshot(screenshot):
    """Save the screenshot to the SCREENSHOTS directory with an incremental filename."""
    next_num = get_next_screenshot_number()
    screenshot_path = os.path.join(SCREENSHOTS_DIR, f'ITEM_{next_num}.png')
    
    # Convert the screenshot from RGB to BGR before saving
    screenshot_bgr = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    cv2.imwrite(screenshot_path, screenshot_bgr)
    
    print(f"Screenshot saved as {screenshot_path}")
    return screenshot_path

def load_screenshot(screenshot_path):
    """Load a screenshot from the specified path."""
    if not os.path.exists(screenshot_path):
        raise FileNotFoundError(f"Screenshot file not found: {screenshot_path}")
    return np.array(Image.open(screenshot_path))

def capture_and_extract(save_screen=True, load_screenshot_path=None):
    """Capture or load a screenshot, process it, and optionally save it."""
    if load_screenshot_path:
        # Load the screenshot from the specified path
        screenshot = load_screenshot(load_screenshot_path)
    else:
        # Capture the screenshot
        screenshot = np.array(sct.grab(sct.monitors[0]))

    if save_screen:
        # Save the screenshot
        save_screenshot(screenshot)

    # Rest of your existing code
    gray_img = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray_img, threshold1=80, threshold2=220)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    annotated_image = screenshot.copy()
    detected_regions = []
    item_info = {}
    res = "Not detected"

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if 400 < w < 600 and 300 < h < 1150:
            cv2.rectangle(annotated_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            region_of_interest = screenshot[y:y + h, x:x + w]
            detected_regions.append(region_of_interest)
            results = ocr.ocr(region_of_interest, cls=False)
            lines = []
            if results[0]:
                for line in results[0]:
                    text, confidence = line[1][0], line[1][1]
                    lines.append(text.strip())
                    print(f"Detected Text: '{text.strip()}' (Confidence: {confidence:.2f})")
                res = check_secondary_prices(lines)
                break
            else:
                print("No text detected in this region.")

    if PLT_EN:
        plt.figure(figsize=(10, 6))
        plt.imshow(cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB))
        plt.title("Full Screen Capture with Detected Boxes")
        plt.axis('off')
        plt.show()

        for idx, region in enumerate(detected_regions):
            plt.figure()
            plt.imshow(cv2.cvtColor(region, cv2.COLOR_BGR2RGB))
            plt.title(f"Detected Region {idx + 1}")
            plt.axis('off')
            plt.show()

    return res


if __name__ == "__main__":
    print("Press Ctrl + 9 to capture the screen. Press 'q' to quit.")
    queue = Queue()
    overlay_process = start_overlay(queue)
    show_text(queue, "Ready!", 10)
    
    while True:
        if keyboard.is_pressed("ctrl+9"):
            show_text(queue, "Capturing screen...", 10)
            print("Capturing screen...")
            str_res = capture_and_extract()
            show_text(queue, str_res, 120)

        if keyboard.is_pressed("q"):
            print("Exiting...")
            overlay_process.terminate()
            break