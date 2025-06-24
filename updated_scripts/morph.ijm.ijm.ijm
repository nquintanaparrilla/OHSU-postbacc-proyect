segmentedDir = "Z:/rawdata/mouse_breast/MFT_C3Tag/TU00801_data/segmented_TU00801/";
morphDir = "Z:/rawdata/mouse_breast/MFT_C3Tag/TU00801_data/morphology_TU00801/";

File.makeDirectory(morphDir);
listdir = getFileList(segmentedDir);

for (i = 0; i < listdir.length; i++) {
    segmentedFolder = segmentedDir + listdir[i];
    segmentedFiles = getFileList(segmentedFolder);
    
    if (segmentedFiles.length == 0) {
        print("No image sequence found in: " + segmentedFolder);
        continue;
    }

    imageBaseName = listdir[i];
    if (endsWith(imageBaseName, "/")) {
        imageBaseName = substring(imageBaseName, 0, lengthOf(imageBaseName) - 1);
    }

    run("Image Sequence...", "open=[" + segmentedFolder + "] sort");
    selectWindow(imageBaseName);
    setAutoThreshold("Mean dark no-reset");
    run("Set Measurements...", "perimeter feret's limit display redirect=None decimal=3");
    run("Analyze Particles...", "size=100-10000 pixel summarize stack");

    // Save results in the morphology directory with dynamic filenames
    saveAs("Results", morphDir + "Summary_of_" + imageBaseName + ".csv"); 
    selectWindow("Summary_of_" + imageBaseName + ".csv");
    run("Close");
    run("Close All");
}
