import os
import shutil
import re
raw_folder = "/mnt/c/Users/natal/Downloads/Raw/"
output_folder = "/mnt/c/Users/natal/Downloads/Sorted_Raw/"

os.makedirs(output_folder, exist_ok=True)

pattern = re.compile(r'([A-D]\d+_\d+)')

file_list = os.listdir(raw_folder)
for file in file_list:
    if file.endswith('.tif'):  
        match = pattern.search(file)
        if match:
            well_number = match.group(1)  # Extract the well number
            well_folder = os.path.join(output_folder, well_number)
            os.makedirs(well_folder, exist_ok=True)

            source_file = os.path.join(raw_folder, file)
            destination_file = os.path.join(well_folder, file)
            shutil.move(source_file, destination_file)
        else:

print('Files sorted successfully.')
