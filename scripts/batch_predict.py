import sys
import joblib
import pandas as pd

MODEL_PATH = "/home/project/FraudDetection/models/xgboost_model.joblib"
model = joblib.load(MODEL_PATH)

input_csv = sys.argv[1]
output_csv = sys.argv[2]

data = pd.read_csv(input_csv)

predictions = model.predict(data)
probability = model.predict_proba(data)[:,1]

data["Prediction"] = predictions
data["Fraud_Probability"] = probability

data.to_csv(output_csv, index=False)

print("Batch prediction completed.")
print("Output:", output_csv)


