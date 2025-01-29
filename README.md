# Image Analysis Pipeline 

## Postbacc project summary:

## 1. Sorting 
For personal preference, I organized all of the raw images obtained by the IncuCyte using [raw_sort.py](image_analysis/raw_sort.py). This sorted all the raw images into their respective folders following by the well plate's letter, well number and region of interest (ROI).

![alt text](https://github.com/nquintanaparrilla/OHSU-postbacc-proyect/blob/d82a9f91822014748dbf2f14079faa0709c2cf97/images/sorting_example.png)
Figure 1. An IncuCyte S3 imaged 36 regions of interest (ROIs) of 16 wells every 30 minutes for 48 hours resulting in 55,872 live-cell images. The labeling image format indicates the well, the ROI and the time interval. So, for the example, the label indicates that the image belongs to the A1 well, it was taken on first ROI and the time interval indicates 4 hours and 30 minutes.

## 2. Stabilizing
A FIJI macro script uses the StackReg and TurboReg plugins register all images like an image sequence and reduce shakiness. It facilitates cell visualization when observation proliferation over time. This is necessary because every image taken at the same ROI, regardless of the interval, will be positioned slightly differently due to the IncuCyte S3’s processing and camera positioning, and it helps the Cellpose model segment more efficiently.



## 3. Cropping

## 4. Quality Control

## 5. Segmentation

## 6. Counting

## References:
cite Fiji, Stackreg, Turboreg, cellpose, sean's paper
# Future optimization objectives:
