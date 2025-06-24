import os
import shutil
import re

def sort_exported_incucyte_images(experiment_plate):
    raw_folder = f'Z:/rawdata/mouse_breast/MFT_C3Tag/INCUCYTE/{experiment_plate}'
    output_folder = f'Z:/rawdata/mouse_breast/MFT_C3Tag/{experiment_plate}_data/sorted_{experiment_plate}'

    os.makedirs(output_folder, exist_ok=True)

    pattern = re.compile(r'([A-H]\d+_\d+)')

  
    file_list = os.listdir(raw_folder)

    for file in file_list:
        
        if file.endswith('.tif'):
            print(f"Processing file: {file}\n")
            
            match = pattern.search(file)
            if match:
                well_number = match.group(1)  # Extract well number 
                well_folder = os.path.join(output_folder, well_number)
                
                # Create the folder for this well number if it doesn't exist
                os.makedirs(well_folder, exist_ok=True)
                
                # Define the source and destination file paths
                source_file = os.path.join(raw_folder, file)  # Use original name to find the source
                destination_file = os.path.join(well_folder, file)  # Keep the file name unchanged
                
                if os.path.exists(destination_file):
                    print(f"File {file} already exists in {well_folder}, deleting from raw folder...\n")
                    os.remove(source_file)
                    print(f"Deleted {file} from {raw_folder}\n")
                    continue  
                
                shutil.move(source_file, destination_file)
                print(f"Moved {file} to {well_folder}\n")
            else:
                print(f"Pattern not found for file: {file}\n")

sort_exported_incucyte_images(experiment_plate='TU00901')