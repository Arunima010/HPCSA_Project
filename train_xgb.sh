#!/bin/bash

#SBATCH --job-name=xgboost_training
#SBATCH --partition=compute
#SBATCH --nodes=2
#SBATCH --ntasks=2
#SBATCH --cpus-per-task=2
#SBATCH --time=02:00:00
#SBATCH --output=/home/project/FraudDetection/logs/xgb_%j.out
#SBATCH --error=/home/project/FraudDetection/logs/xgb_%j.err

echo "========================================"
echo "XGBoost Training Started"
echo "Date : $(date)"
echo "Node : $(hostname)"
echo "========================================"

source /home/project/fraud_env/bin/activate

python /home/project/FraudDetection/scripts/train_xgboost.py

echo "========================================"
echo "Training Finished"
echo "Date : $(date)"
echo "========================================"
