#!/bin/bash

#SBATCH --job-name=aply_dnn
#
#SBATCH --partition=normal
#
#SBATCH --ntasks=1
#
#SBATCH --cpus-per-task=2
#
#SBATCH --gres=gpu:1
#
#SBATCH --output=slurm.out
#

python3 apply_dnn.py
