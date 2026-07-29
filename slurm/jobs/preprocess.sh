#!/bin/bash
#SBATCH --job-name=preprocess
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --time=00:20:00
#SBATCH --output=/home/project/FraudDetection/slurm/logs/preprocess_%j.out
#SBATCH --error=/home/project/FraudDetection/slurm/logs/preprocess_%j.err

echo "======================================="
echo " PREPROCESSING JOB STARTED"
echo " Host: $(hostname)"
echo " Date: $(date)"
echo "======================================="

source /home/project/fraud_env/bin/activate
python /home/project/FraudDetection/scripts/preprocess.py

echo "======================================="
echo " PREPROCESSING COMPLETED"
echo " Date: $(date)"
echo "======================================="
