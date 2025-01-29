# This script runs faster in a virtual cluster
import cv2
import os
import numpy as np
import shutil

def find_common_bounding_box(image_files):
    """
    Find the common bounding box that fits non-white regions across all frames.
    """
    x_min, y_min, x_max, y_max = None, None, None, None
    
    for file in image_files:
        img = cv2.imread(file)
        if img is None:
            print(f"Failed to load image: {file}")
            continue  # Skip to the next image

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Threshold to detect non-white areas (assuming white is close to 255)
        _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
        
        # Find the contours of non-white areas
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Get bounding box for the current frame
            x, y, w, h = cv2.boundingRect(contours[0])
            
            # Update the common bounding box
            if x_min is None:
                x_min, y_min, x_max, y_max = x, y, x + w, y + h
            else:
                x_min = max(x_min, x)
                y_min = max(y_min, y)
                x_max = min(x_max, x + w)
                y_max = min(y_max, y + h)
    
    return x_min, y_min, x_max, y_max

def crop_images_to_bounding_box(image_files, crop_box, save_dir, not_cropped_dir, subdir):
    """
    Crop images to the common bounding box and save them, or move files if the box is invalid.
    """
    x_min, y_min, x_max, y_max = crop_box
    
    # Check if the cropping box is valid
    if x_min is None or x_min >= x_max or y_min >= y_max:
        print(f"Invalid crop box found in all images for {subdir}. Moving files to not_cropped_dir.")
        os.makedirs(not_cropped_dir, exist_ok=True)
        for file in image_files:
            shutil.copy(file, not_cropped_dir)
        return False  

    for file in image_files:
        img = cv2.imread(file)
        if img is None:
            print(f"Failed to load image: {file}. Skipping...")
            continue 

        # Crop the image using the bounding box
        cropped_img = img[y_min:y_max, x_min:x_max]

        # Check if the cropped image is valid 
        if cropped_img.size == 0:
            print(f"Cropped image is empty for: {file}. Skipping...")
            continue

        save_path = os.path.join(save_dir, os.path.basename(file))
        cv2.imwrite(save_path, cropped_img)

    return True  


def crop_stabilized_images(experiment_plate):
    stabilized_dir = f'/path/to/stabilized/images/{experiment_plate}_data/stabilized_{experiment_plate}/'
    cropped_dir = f'/path/to/stabilized/images/{experiment_plate}_data/cropped_{experiment_plate}/' # output for successfully cropped images
    not_cropped_dir = f'/path/to/stabilized/images/{experiment_plate}_data/not_cropped_{experiment_plate}/' #output folder for unsuccessfully cropped images
    qc_dir = f'/path/to/stabilized/images/{experiment_plate}_data/cropped_{experiment_plate}/' #creates an empty folder in the cropped dir 

    os.makedirs(qc_dir, exist_ok=True)

    for subdir in os.listdir(stabilized_dir):
        subdir_path = os.path.join(stabilized_dir, subdir)
        print(f"Processing {subdir}")
        
        if os.path.isdir(subdir_path):
            cropped_subdir = os.path.join(cropped_dir, subdir)
            not_cropped_subdir = os.path.join(not_cropped_dir, subdir)
            qc_subdir = os.path.join(qc_dir, subdir)
            
            # Skip if the cropped subdir already exists just in case the script is interrupted
            if os.path.exists(cropped_subdir) and os.listdir(cropped_subdir):
                print(f"Subdirectory {cropped_subdir} already exists. Skipping...\n")
                continue  # Skip to the next subdirectory
            
            # Collect image files in the sequence
            image_files = [os.path.join(subdir_path, f) for f in os.listdir(subdir_path) if f.endswith('.tif')]
            
            # Condition 1: Check if subdir contains less than 97 image files. This is specific to my project since the total images in each subdir for me should be 97. The number should be modified to the number of files each dir should have.
            if len(image_files) < 97:
                print(f"{subdir} contains only {len(image_files)} image files. Skipping for now...\n")
                continue
            
            if image_files:
                # Find the common bounding box across all frames
                crop_box = find_common_bounding_box(image_files)
                
                # Create the cropped subdirectory if it doesn't exist
                os.makedirs(cropped_subdir, exist_ok=True)
                
                # Crop all images to the common bounding box or move if invalid box
                success = crop_images_to_bounding_box(image_files, crop_box, cropped_subdir, not_cropped_subdir, subdir)
                
                if not success:
                    # Create an empty subdir in QC for the invalid cases
                    os.makedirs(qc_subdir, exist_ok=True)
                    print(f"Created empty QC subdir for {subdir}.\n")
                else:
                    print(f"Cropped {subdir}\n")

crop_stabilized_images(experiment_plate = 'MC00701')
