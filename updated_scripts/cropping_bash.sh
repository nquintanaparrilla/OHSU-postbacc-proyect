#!/bin/bash
#SBATCH -p gpu
#SBATCH --gres=gpu:1
#SBATCH --time=8:00:00

module load miniconda3
eval "$(conda shell.bash hook)"
conda activate cellpose-env
srun python cropping.py