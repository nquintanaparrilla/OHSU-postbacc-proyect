#!/bin/bash
#SBATCH -p gpu
#SBATCH --gres=gpu:1
#SBATCH --time=36:00:00

module load miniconda3
eval "$(conda shell.bash hook)"
conda activate cellpose-env
srun python cellpose_segmentation.py