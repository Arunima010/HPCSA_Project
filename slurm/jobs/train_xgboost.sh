#!/bin/bash
#SBATCH --job-name=train_xgboost
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --time=02:00:00
#SBATCH --output=/home/project/FraudDetection/slurm/logs/train_xgboost_%j.out
#SBATCH --error=/home/project/FraudDetection/slurm/logs/train_xgboost_%j.err

source /home/project/fraud_env/bin/activate

python /home/project/FraudDetection/scripts/train_xgboost.py
