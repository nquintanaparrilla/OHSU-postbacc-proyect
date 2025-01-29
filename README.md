# Image Analysis Pipeline 

## Postbacc project summary:

## 1. Sorting ([raw_sort.py](image_analysis/raw_sort.py))
For personal preference, I organized all of the raw images obtained by the IncuCyte using this script. This sorted all the raw images into their respective folders following by the well plate's letter, well number and region of interest (ROI).

![alt text](https://github.com/nquintanaparrilla/OHSU-postbacc-proyect/blob/d82a9f91822014748dbf2f14079faa0709c2cf97/images/sorting_example.png)
Figure 1. An IncuCyte S3 imaged 36 regions of interest (ROIs) of 16 wells every 30 minutes for 48 hours resulting in 55,872 live-cell images. The labeling image format indicates the well, the ROI and the time interval. So, for the example, the label indicates that the image belongs to the A1 well, it was taken on first ROI and the time interval indicates 4 hours and 30 minutes.

## 2. Stabilizing ([stabilize.ijm](image_analysis/stabilize.ijm))
A [FIJI](https://imagej.net/software/fiji/) macro script uses the [StackReg](https://bigwww.epfl.ch/thevenaz/stackreg/) and [TurboReg](https://bigwww.epfl.ch/thevenaz/turboreg/) plugins register all images like an image sequence and reduce shakiness. It facilitates cell visualization when observation proliferation over time. This is necessary because every image taken at the same ROI, regardless of the interval, will be positioned slightly differently due to the IncuCyte S3’s processing and camera positioning, and it helps the Cellpose model segment more efficiently.

<img src="images/A2_1_sorted.gif" width="0=400" height="400">
Figure 2. Image sequence A2_1 before stabilizing step.


<img src="images/A2_1_stabilized.gif" width="500" height="400">
Figure 3. Image sequence A2_1 after stabilizing step.


<img src="images/stabilizing_example.png" width="900" height="500">
Figure 4. A side-by-side image sequence comparison on the first 3 30-minute intervals of the first ROI in the A1 well. The white background indicates how the image was moved to maintain consistency. This is the white box the the cropping step will find to crop.

## 3. Cropping ([cropping.py](image_analysis/cropping.py))
This python script  crops the white background created when the images were moved in frame to be stabilized. This script can also indicate if an image sequence was stabilized incorrectly due to debris or additional noise, which can interfere with the FIJI plugins.

## 4. Quality Control

## 5. Segmentation

## 6. Counting

## References:
cite Fiji, Stackreg, Turboreg, cellpose, sean's paper
# Future optimization objectives:
