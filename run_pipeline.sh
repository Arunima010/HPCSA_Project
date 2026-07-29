#!/bin/bash
PRE=$(sbatch --parsable slurm/jobs/preprocess.sh)

FE=$(sbatch --parsable --dependency=afterok:$PRE slurm/jobs/feature_engineering.sh)

PT=$(sbatch --parsable --dependency=afterok:$FE slurm/jobs/prepare_training.sh)

TR=$(sbatch --parsable --dependency=afterok:$PT slurm/jobs/train_xgboost.sh)

echo "Pipeline Submitted"
echo "Preprocess Job : $PRE"
echo "Feature Engineering Job : $FE"
echo "Prepare Training Job : $PT"
echo "Training Job : $TR"
