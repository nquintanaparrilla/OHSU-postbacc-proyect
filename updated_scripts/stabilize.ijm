rawDir = File.getDirectory("Z:/rawdata/mouse_breast/MFT_C3Tag/TU00901_data/sorted_TU00901/*");
stabilizedDir = File.getDirectory("Z:/rawdata/mouse_breast/MFT_C3Tag/TU00901_data/stabilized_TU00901/*");
File.makeDirectory(stabilizedDir);
listdir = getFileList(rawDir);

for(i=0; i < listdir.length; i++) {
	currentStabilizedFolder = stabilizedDir + listdir[i];
    
    if (File.exists(currentStabilizedFolder)) {
        print("Skipping existing directory: " + currentStabilizedFolder);
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
	run("Properties...", "channels=1 slices=1 frames=73 unit=pixel pixel_width=1.0000 pixel_height=1.0000 voxel_depth=1.0000 frame=[60 min]");
    //run("Invert", "stack");
    run("Image Sequence... ", "format=TIFF save=&stabilizedFolder");
    close();
	}