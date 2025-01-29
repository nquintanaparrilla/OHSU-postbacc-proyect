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
def summarize_ROIs(experiment_plate, rois):
    '''
    Sums up all the cell counts of all ROIS in one well.
    '''
    input_csv_file = f"/path/to/{experiment_plate}/{experiment_plate}_masks_report.csv"
  
    output_csv_file = f"/path/to/{experiment_plate}/{experiment_plate}_{rois}ROIs.csv"

    # Well name prefixes to check. Modify list to include the wells that were used in the experiment plate. For example, my experiments were conducted in 24-well plates but I only used the wells listed below.
    well_names = ["A2", "A3", "A4", "A5", 
                  "B2", "B3", "B4", "B5",
                  "C2", "C3", "C4", "C5", 
                  "D2", "D3", "D4", "D5"]

    # Suffixes (ROIs) to consider: Modify list to include only the ROIs you're interested in. With this list it will only summarize 14/36 ROIs
    suffix_list = ["_1", "_2", "_3", "_4", "_5", "_6", "_7", "_30", "_31", "_32", "_33", "_34", "_35", "_36"]

    # Initialize a dictionary to store summed values for each well
    summed_data = {well: [0] * 97 for well in well_names} 

    # Read the input CSV file
    with open(input_csv_file, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Skip the header row
        
        # Process each row
        for row in reader:
            well_name = row[0]
            
            # Check if well_name has a valid prefix and suffix
            for well in well_names:
                if well_name.startswith(well) and any(well_name.endswith(suffix) for suffix in suffix_list):
                    # Convert remaining items in row to float and add them to corresponding position
                    values = list(map(float, row[1:]))  # Skip the index column and get values
                    summed_data[well] = [summed_data[well][i] + values[i] for i in range(len(values))]

    # Write the results to a new CSV file
    with open(output_csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        
        # Write headers
        writer.writerow(["Well Name", "0", "0.5", "1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5", "5.5", "6", "6.5", "7", "7.5", "8", "8.5", "9", "9.5", "10", "10.5", "11", "11.5", "12", "12.5", "13", "13.5", "14", "14.5", "15", "15.5", "16", "16.5", "17", "17.5", "18", "18.5", "19", "19.5", "20", "20.5", "21", "21.5", "22", "22.5", "23", "23.5", "24", "24.5", "25", "25.5", "26", "26.5", "27", "27.5", "28", "28.5", "29", "29.5", "30", "30.5", "31", "31.5", "32", "32.5", "33", "33.5", "34", "34.5", "35", "35.5", "36", "36.5", "37", "37.5", "38", "38.5", "39", "39.5", "40", "40.5", "41", "41.5", "42", "42.5", "43", "43.5", "44", "44.5", "45", "45.5", "46", "46.5", "47", "47.5", "48"])
        
        # Write the summed data for each well name
        for well, values in summed_data.items():
            writer.writerow([well] + values)

    print(f"Data processing complete. Output saved to {output_csv_file}")

count_masks_as_cells(experiment_plate='MC01701')
summarize_ROIs(experiment_plate='MC01701', rois = 36)
