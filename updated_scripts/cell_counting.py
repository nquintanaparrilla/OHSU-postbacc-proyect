import os
import numpy as np
import pandas as pd
from skimage import io

# Your existing function
def count_masks_from_segmentation(image_path):
    mask_image = io.imread(image_path)
    unique_masks = np.unique(mask_image)
    num_masks = len(unique_masks) - 1 if 0 in unique_masks else len(unique_masks)
    return num_masks

def count_masks_as_cells (experiment_plate):
    segmented_dir = f'/path/to/your/folder/{experiment_plate}_data/segmented_{experiment_plate}/'

    subdirs = sorted(os.listdir(segmented_dir))
    data = {}
    max_length = 0

    for subdir in subdirs:
        subdir_path = os.path.join(segmented_dir, subdir)
        print(f"Processing {subdir}")

        # Get and sort image files
        image_files = sorted(f for f in os.listdir(subdir_path) if f.endswith('.tif'))

        # Count masks for each image
        mask_counts = [count_masks_from_segmentation(os.path.join(subdir_path, f)) for f in image_files]
        data[subdir] = mask_counts

        if len(mask_counts) > max_length:
            max_length = len(mask_counts)

    # Build and save the DataFrame
    df = pd.DataFrame({key: pd.Series(val) for key, val in data.items()})
    output_csv_path = os.path.join(segmented_dir, f'/path/to/your/folder/{experiment_plate}_data/{experiment_plate}_cell_counts.csv')
    df.to_csv(output_csv_path, index=False)

    print(f"Saved test summary to: {output_csv_path}")

count_masks_as_cells("TU00901")
