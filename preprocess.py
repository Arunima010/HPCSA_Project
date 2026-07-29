import pandas as pd
import os

# -------------------------
# Paths
# -------------------------

DATA_DIR = "/home/project/FraudDetection/data"
RESULT_DIR = "/home/project/FraudDetection/results"

os.makedirs(RESULT_DIR, exist_ok=True)

print("="*60)
print("Loading datasets...")
print("="*60)

transaction = pd.read_csv(f"{DATA_DIR}/train_transaction.csv")
identity = pd.read_csv(f"{DATA_DIR}/train_identity.csv")

print("Transaction Shape :", transaction.shape)
print("Identity Shape    :", identity.shape)

print("\nMerging datasets on TransactionID...")

df = transaction.merge(identity,
                       how="left",
                       on="TransactionID")

print("Merged Shape :", df.shape)

print("\nSaving merged dataset...")

df.to_csv(f"{RESULT_DIR}/merged_dataset.csv",
          index=False)

print("Done.")

print("\nFirst 5 rows:")

print(df.head())
