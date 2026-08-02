from pathlib import Path
import pandas as pd

BASE_DIR = Path("/home/project/FraudDetection")

prediction_dir = BASE_DIR / "predictions"

merged_dir = BASE_DIR / "merged"

merged_dir.mkdir(exist_ok=True)

files = sorted(prediction_dir.glob("*_prediction.csv"))

if len(files) == 0:
    print("No prediction files found.")
    exit()

dfs = []

for file in files:
    print(f"Reading {file.name}")
    dfs.append(pd.read_csv(file))

merged = pd.concat(dfs, ignore_index=True)

output = merged_dir / "predictions.csv"

merged.to_csv(output, index=False)

print(f"Merged {len(files)} files.")

print(f"Saved to {output}")


