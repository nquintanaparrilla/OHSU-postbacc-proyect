# This can be run locally but it can take up to 5 hours. The script has to be modified to run on the cluster because when it runs on the cluster, the outputs aren't the real results (don't match sample ground truths).
import os
import numpy as np
from skimage import io  
import csv


def count_masks_from_segmentation(image_path):
  '''
  Counts all the masks in one image (ROI)
  '''
    mask_image = io.imread(image_path)
    unique_masks = np.unique(mask_image)
    num_masks = len(unique_masks) - 1 if 0 in unique_masks else len(unique_masks)
    return num_masks

def count_masks_as_cells(experiment_plate):
  '''
  Saves cells counts for each individual ROI. 
  '''
    segmented_dir = f"/path/to/{experiment_plate}_data/segmented_{experiment_plate}"
    output_csv = f"/path/to/{experiment_plate}/{experiment_plate}_masks_report.csv"
    experiment_plate_dir = f"/path/to/{experiment_plate}"
    os.makedirs(experiment_plate_dir, exist_ok = True)

    csv_data = []

    # Iterate through each subdirectory in the segmented directory
    for subdir in os.listdir(segmented_dir):
        subdir_path = os.path.join(segmented_dir, subdir)
        print(f"Processing {subdir}")

        if os.path.isdir(subdir_path):
            image_files = [f for f in os.listdir(subdir_path) if f.endswith('.tif')]

            mask_counts = [count_masks_from_segmentation(os.path.join(subdir_path, image_file)) for image_file in image_files]

            csv_data.append([subdir] + mask_counts)

    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Creates a time interval for each column. Modify this list if time intervals are different.
        writer.writerow(["Well Name", "0", "0.5", "1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5", "5.5", "6", "6.5", "7", "7.5", "8", "8.5", "9", "9.5", "10", "10.5", "11", "11.5", "12", "12.5", "13", "13.5", "14", "14.5", "15", "15.5", "16", "16.5", "17", "17.5", "18", "18.5", "19", "19.5", "20", "20.5", "21", "21.5", "22", "22.5", "23", "23.5", "24", "24.5", "25", "25.5", "26", "26.5", "27", "27.5", "28", "28.5", "29", "29.5", "30", "30.5", "31", "31.5", "32", "32.5", "33", "33.5", "34", "34.5", "35", "35.5", "36", "36.5", "37", "37.5", "38", "38.5", "39", "39.5", "40", "40.5", "41", "41.5", "42", "42.5", "43", "43.5", "44", "44.5", "45", "45.5", "46", "46.5", "47", "47.5", "48"])  # Adjust the header as needed

        writer.writerows(csv_data)

    print(f"Report saved to {output_csv}")

count_masks_as_cells(experiment_plate='MC01701')
