import sys
import pandas as pd
from pathlib import Path
import joblib
import socket


BASE_DIR = Path("/home/project/FraudDetection")
MODEL = joblib.load(BASE_DIR / "models" / "xgboost_model.joblib")

chunk_file = Path(sys.argv[1])

df = pd.read_csv(chunk_file)

predictions = MODEL.predict(df)
probabilities = MODEL.predict_proba(df)[:, 1]

df = df.copy()
df["Prediction"] = predictions
df["Fraud_Probability"] = probabilities
df["ComputeNode"] = socket.gethostname()
print(f"Processed {chunk_file.name} on node: {socket.gethostname()}")


output_dir = BASE_DIR / "predictions"
output_dir.mkdir(exist_ok=True)

output_file = output_dir / f"{chunk_file.stem}_prediction.csv"

df.to_csv(output_file, index=False)

print(f"Finished {chunk_file.name}")
