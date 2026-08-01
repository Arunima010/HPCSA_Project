import sys
import pandas as pd
from pathlib import Path

chunk_file = Path(sys.argv[1])

df = pd.read_csv(chunk_file)

output_dir = Path("/home/project/FraudDetection/predictions")
output_dir.mkdir(exist_ok=True)

output_file = output_dir / f"{chunk_file.stem}_prediction.csv"

df.to_csv(output_file, index=False)

print(f"Processed {chunk_file.name}")
