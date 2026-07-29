#!/bin/bash
#SBATCH --job-name=feature_engineering
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --time=00:30:00
#SBATCH --output=/home/project/FraudDetection/slurm/logs/feature_engineering_%j.out
#SBATCH --error=/home/project/FraudDetection/slurm/logs/feature_engineering_%j.err

source /home/project/fraud_env/bin/activate

python /home/project/FraudDetection/scripts/feature_engineering.py
