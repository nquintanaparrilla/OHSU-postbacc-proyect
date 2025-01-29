// Let run overnight since it interacts with the GUI. This script was originally written within the Heiser Lab with my own minor modifictions.
rawDir = File.getDirectory("/path/to/sorted/folder/MC00701_data/sorted_MC00701/*");
stabilizedDir = File.getDirectory("/path/to/stabilized/output/folder/MC00701_data/stabilized_MC00701/*");
File.makeDirectory(stabilizedDir);
listdir = getFileList(rawDir);

for(i=0; i < listdir.length; i++) {
	currentStabilizedFolder = stabilizedDir + listdir[i];
    
    if (File.exists(currentStabilizedFolder)) {
        print("Skipping existing directory: " + currentStabilizedFolder); // this helps incase the script is interrupted for any reason
        continue;
    }
	print("Processing: " + rawDir + listdir[i]);
	File.makeDirectory(stabilizedDir + listdir[i]);
	rawFolder = rawDir + listdir[i];
	stabilizedFolder = stabilizedDir + listdir[i];
	rawFiles = getFileList(rawFolder);
	rawFile = rawFolder + rawFiles[0];
	run("Image Sequence...", "open=&rawFile");
	rename("1");
	run("Duplicate...", "duplicate");selectWindow("1-1");run("Enhance Contrast...", "saturated=1 process_all");run("Find Edges", "stack");run("Merge Channels...", "c1=1 c2=1-1 keep");selectWindow("1");close();selectWindow("1-1");close();
	run("StackReg ", "transformation=Translation");run("Split Channels");selectWindow("RGB (green)");close();selectWindow("RGB (blue)");close();
	run("Properties...", "channels=1 slices=1 frames=97 unit=pixel pixel_width=1.0000 pixel_height=1.0000 voxel_depth=1.0000 frame=[30 min]");
  run("Invert", "stack");
  run("Image Sequence... ", "format=TIFF save=&stabilizedFolder");
  close();
	}
