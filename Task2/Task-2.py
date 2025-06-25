#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
import os
import numpy as np
from IPython.display import display, Image

def detect_changes(before_img, after_img):
    # Convert to grayscale
    gray_before = cv2.cvtColor(before_img, cv2.COLOR_BGR2GRAY)
    gray_after = cv2.cvtColor(after_img, cv2.COLOR_BGR2GRAY)

    # Compute absolute difference
    diff = cv2.absdiff(gray_before, gray_after)

    # Threshold the difference
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

    # Morphological operations to remove noise
    kernel = np.ones((5,5), np.uint8)
    thresh = cv2.dilate(thresh, kernel, iterations=2)
    thresh = cv2.erode(thresh, kernel, iterations=1)

    # Find contours of changed areas
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw bounding boxes on the "after" image
    result = after_img.copy()
    for cnt in contours:
        if cv2.contourArea(cnt) > 500:  # filter small changes
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(result, (x, y), (x + w, y + h), (0, 0, 255), 2)

    return result

def process_change_detection(input_folder, output_folder):
    all_files = [f for f in os.listdir(input_folder) if f.endswith('.jpg')]
    before_images = [f for f in all_files if '~2' not in f]

    print("📂 Found before images:", before_images)

    for before_file in before_images:
        id_name = before_file.split('.')[0]
        after_file = f"{id_name}~2.jpg"

        before_path = os.path.join(input_folder, before_file)
        after_path = os.path.join(input_folder, after_file)

        if not os.path.exists(after_path):
            print(f"❌ After image not found for: {before_file}")
            continue

        before_img = cv2.imread(before_path)
        after_img = cv2.imread(after_path)

        if before_img is None or after_img is None:
            print(f"❌ Could not load image pair: {before_file}, {after_file}")
            continue

        result = detect_changes(before_img, after_img)

        out_path = os.path.join(output_folder, f"{id_name}_changes.jpg")
        cv2.imwrite(out_path, result)
        print(f"✅ Saved: {out_path}")
        display(Image(filename=out_path))  # shows in Jupyter

# ---- FOLDER PATHS ---- #
input_dir = r"C:\Users\SHWETA BISHT\Downloads\input-images"
output_dir = r"C:\Users\SHWETA BISHT\Downloads\change-detection-output"
os.makedirs(output_dir, exist_ok=True)

# ---- RUN ---- #
process_change_detection(input_dir, output_dir)

