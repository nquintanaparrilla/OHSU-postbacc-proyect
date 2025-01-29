import os
import shutil
import re


def sort_exported_incucyte_images(experiment_plate):
    raw_folder = f'/path/to/exported/images{experiment_plate}' #input the name of the folder. For my project my first experiment plate was called MC00701
    output_folder = f'/path/to/output/folder/{experiment_plate}_data/sorted_{experiment_plate}'
    # create the output folder
    os.makedirs(output_folder, exist_ok=True)

    # Pattern to match the IncuCyte's image's labeling
    pattern = re.compile(r'([A-H]\d+_\d+)')

    file_list = os.listdir(raw_folder)
    for file in file_list:
        if file.endswith('.tif'):
            print(f"Processing file: {file}\n")
            match = pattern.search(file)
            if match:
                well_number = match.group(1)  # extract well number (e.g., A1_01)
                well_folder = os.path.join(output_folder, well_number)
                
                # creates the folder for this well number if it doesn't exist
                os.makedirs(well_folder, exist_ok=True)
               
                source_file = os.path.join(raw_folder, file)  # Use original name to find the source
                destination_file = os.path.join(well_folder, file)  # Keep the file name unchanged
                
                # check if the file already exists in the destination. not necessary to keep in the script unless you did multiple exports
                if os.path.exists(destination_file):
                    print(f"File {file} already exists in {well_folder}, deleting from raw folder...\n")
                    os.remove(source_file)
                    print(f"Deleted {file} from {raw_folder}\n")
                    continue  
                
                # Move the file to the new folder
                shutil.move(source_file, destination_file)
                print(f"Moved {file} to {well_folder}\n")
            else:
                print(f"Pattern not found for file: {file}\n")
