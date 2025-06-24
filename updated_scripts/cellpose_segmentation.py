from cellpose import models, io
import os

def cellpose_segmentation(experiment_plate):
    cropped_dir = f'/home/groups/heiserlab_genomics/rawdata/mouse_breast/MFT_C3Tag/{experiment_plate}_data/cropped_{experiment_plate}'
    model_path = f'/home/groups/heiserlab_genomics/rawdata/mouse_breast/MFT_C3Tag/train_model_tumor_cells/models/tumor_CP_model_3'
    segmented_dir = f'/home/groups/heiserlab_genomics/rawdata/mouse_breast/MFT_C3Tag/{experiment_plate}_data/segmented_{experiment_plate}'
    os.makedirs(segmented_dir, exist_ok=True)

    use_gpu = True
    model = models.CellposeModel(gpu=use_gpu, pretrained_model=model_path)

    for subdirectory in os.listdir(cropped_dir):
        subdirectory_path = os.path.join(cropped_dir, subdirectory)
        if os.path.isdir(subdirectory_path):
            print(f"Processing {subdirectory}...")
            output_subdir = os.path.join(segmented_dir, subdirectory)
            # Check if output_subdir already exists
            if os.path.exists(output_subdir):
                print(f"Skipping {subdirectory}, already processed.")
                continue
            image_files = io.get_image_files(subdirectory_path, mask_filter="", look_one_level_down=True)
            for image_file in image_files:
                image = io.imread(os.path.join(subdirectory_path, image_file)) 
                result = model.eval(image, diameter=0, channels=[0,0])
                if len(result) == 4:
                    masks, flows, styles, diams = result
                else:
                    masks, flows, styles = result
                    diams = None

                os.makedirs(output_subdir, exist_ok=True)
                io.save_masks(images=image, masks=masks, flows=flows, tif=True, savedir=output_subdir, file_names=image_file, png=False)
                print(f"saved {image_file} in {output_subdir}")

cellpose_segmentation('TU00901')