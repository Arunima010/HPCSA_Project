import pandas as pd
import joblib
import os

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

RESULT_DIR = "/home/project/FraudDetection/results"

print("=" * 60)
print("Loading cleaned dataset...")
print("=" * 60)

df = pd.read_csv(f"{RESULT_DIR}/cleaned_dataset.csv")

print("Dataset Shape:", df.shape)

# -------------------------
# Remove identifier
# -------------------------

if "TransactionID" in df.columns:
    df.drop(columns=["TransactionID"], inplace=True)

# -------------------------
# Target
# -------------------------

y = df["isFraud"]

X = df.drop(columns=["isFraud"])

print("Features:", X.shape)
print("Target:", y.shape)

# -------------------------
# Encode categorical columns
# -------------------------

encoders = {}

cat_cols = X.select_dtypes(include=["object"]).columns

print(f"Encoding {len(cat_cols)} categorical columns...")

for col in cat_cols:

    le = LabelEncoder()

    X[col] = le.fit_transform(X[col].astype(str))

    encoders[col] = le

print("Encoding Complete.")

# -------------------------
# Train Test Split
# -------------------------

X_train, X_valid, y_train, y_valid = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining Shape :", X_train.shape)
print("Validation Shape :", X_valid.shape)

# -------------------------
# Save datasets
# -------------------------

X_train.to_csv(f"{RESULT_DIR}/X_train.csv", index=False)
X_valid.to_csv(f"{RESULT_DIR}/X_valid.csv", index=False)

y_train.to_csv(f"{RESULT_DIR}/y_train.csv", index=False)
y_valid.to_csv(f"{RESULT_DIR}/y_valid.csv", index=False)

joblib.dump(encoders, f"{RESULT_DIR}/label_encoders.pkl")

print("\nTraining datasets saved successfully.")
