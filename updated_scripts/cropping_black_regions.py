import cv2
import os
import numpy as np
import shutil

def find_common_bounding_box(image_files):
    """
    Find the common bounding box that fits non-black regions across all frames.
    """
    x_min, y_min, x_max, y_max = None, None, None, None
    
    for file in image_files:
        img = cv2.imread(file)
        if img is None:
            print(f"Failed to load image: {file}")
            continue  # Skip to the next image

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Threshold to detect non-black areas (assuming black is close to 0)
        _, thresh = cv2.threshold(gray, 15, 255, cv2.THRESH_BINARY)
        
        # Find the contours of non-black areas
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
        return False  # Return False to indicate invalid cropping

    for file in image_files:
        img = cv2.imread(file)
        if img is None:
            print(f"Failed to load image: {file}. Skipping...")
            continue  # Skip to the next image

        # Crop the image using the bounding box
        cropped_img = img[y_min:y_max, x_min:x_max]

        # Check if the cropped image is valid
        if cropped_img.size == 0:
            print(f"Cropped image is empty for: {file}. Skipping...")
            continue

        # Save the cropped image
        save_path = os.path.join(save_dir, os.path.basename(file))
        cv2.imwrite(save_path, cropped_img)

    return True  # Return True to indicate successful cropping


def crop_stabilized_images(experiment_plate):
    stabilized_dir = f'Z:/rawdata/mouse_breast/MFT_C3Tag/{experiment_plate}_data/stabilized_{experiment_plate}/'
    cropped_dir = f'Z:/rawdata/mouse_breast/MFT_C3Tag/{experiment_plate}_data/cropped_{experiment_plate}/'
    not_cropped_dir = f'Z:/rawdata/mouse_breast/MFT_C3Tag/{experiment_plate}_data/not_cropped_{experiment_plate}/'
    qc_dir = f'Z:/rawdata/mouse_breast/MFT_C3Tag/{experiment_plate}_data/cropped_{experiment_plate}/'

    # Ensure the QC directory exists
    os.makedirs(qc_dir, exist_ok=True)
    
    # Loop through each subdirectory in the main directory
    for subdir in os.listdir(stabilized_dir):
        subdir_path = os.path.join(stabilized_dir, subdir)
        print(f"Processing {subdir}")
        
        if os.path.isdir(subdir_path):
            # Create directories for cropped and not cropped images
            cropped_subdir = os.path.join(cropped_dir, subdir)
            not_cropped_subdir = os.path.join(not_cropped_dir, subdir)
            qc_subdir = os.path.join(qc_dir, subdir)
            
            # Skip if the cropped subdir already exists
            if os.path.exists(cropped_subdir) and os.listdir(cropped_subdir):
                print(f"Subdirectory {cropped_subdir} already exists. Skipping...\n")
                continue  # Skip to the next subdirectory
            
            # Collect image files in the sequence
            image_files = [os.path.join(subdir_path, f) for f in os.listdir(subdir_path) if f.endswith('.tif')]
            
            # Condition 1: Check if subdir contains less than 97 image files
            if len(image_files) < 73:
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