#!/bin/bash
#SBATCH --job-name=fraud_predict
#SBATCH --output=logs/predict_%j.out
#SBATCH --error=logs/predict_%j.err
#SBATCH --nodes=1
#SBATCH --ntasks=1

source ~/fraud_env/bin/activate

python3 scripts/predict_chunk.py "$1"
