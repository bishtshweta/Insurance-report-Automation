#!/usr/bin/env python
# coding: utf-8

# In[7]:


import cv2
import os
import numpy as np
from IPython.display import Image, display


def align_and_overlay(rgb_img, thermal_img):
    if thermal_img is None or rgb_img is None:
        print("⚠️ One of the images is None")
        return rgb_img

   
    thermal_resized = cv2.resize(thermal_img, (rgb_img.shape[1], rgb_img.shape[0]))

   
    thermal_colored = cv2.applyColorMap(thermal_resized, cv2.COLORMAP_JET)

    
    gray_rgb = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2GRAY)
    gray_thermal = cv2.cvtColor(thermal_resized, cv2.COLOR_BGR2GRAY)  

    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(gray_rgb, None)
    kp2, des2 = orb.detectAndCompute(gray_thermal, None)

    if des1 is None or des2 is None or len(kp1) < 4 or len(kp2) < 4:
        print("⚠️ Not enough keypoints or descriptors")
        return rgb_img

    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = matcher.match(des2, des1)

    if len(matches) < 4:
        print("⚠️ Not enough matches")
        return rgb_img

    src_pts = np.float32([kp2[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp1[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

    H, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    warped_thermal = cv2.warpPerspective(thermal_colored, H, (rgb_img.shape[1], rgb_img.shape[0]))

    overlay = cv2.addWeighted(rgb_img, 0.6, warped_thermal, 0.4, 0)
    return overlay


def process_images(input_folder, output_folder):
    all_files = os.listdir(input_folder)
    print("📂 Files in input folder:", all_files)

   
    ids = set('_'.join(f.split('_')[:-1]) for f in all_files if f.endswith(('.JPG', '.jpg')))

    for id in ids:
        thermal_path = os.path.join(input_folder, f"{id}_T.JPG")
        rgb_path = os.path.join(input_folder, f"{id}_Z.JPG")

        print(f"\n🔄 Processing ID: {id}")
        print("Thermal exists:", os.path.exists(thermal_path))
        print("RGB exists:", os.path.exists(rgb_path))

        if os.path.exists(thermal_path) and os.path.exists(rgb_path):
            thermal = cv2.imread(thermal_path)
            rgb = cv2.imread(rgb_path)

            if thermal is None or rgb is None:
                print("❌ Failed to load image data")
                continue

            result = align_and_overlay(rgb, thermal)

            out_name = f"{id.split('_')[-1]}_overlay.JPG"
            out_path = os.path.join(output_folder, out_name)
            cv2.imwrite(out_path, result)
            print(f"✅ Saved: {out_path}")

            
            display(Image(filename=out_path))
        else:
            print("❌ Image pair not found for ID:", id)


input_dir = r"C:\Users\SHWETA BISHT\Downloads\input-images"
output_dir = r"C:\Users\SHWETA BISHT\Downloads\output-images\sample-output"
os.makedirs(output_dir, exist_ok=True)


process_images(input_dir, output_dir)

