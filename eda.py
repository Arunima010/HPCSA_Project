import pandas as pd
import os

DATA_DIR = "/home/project/FraudDetection/results"
RESULT_DIR = "/home/project/FraudDetection/results"

os.makedirs(RESULT_DIR, exist_ok=True)

print("="*70)
print("Loading merged dataset...")
print("="*70)

df = pd.read_csv(f"{DATA_DIR}/merged_dataset.csv")

print("\nDataset Shape")
print(df.shape)

print("\nMemory Usage")
print(f"{df.memory_usage(deep=True).sum()/1024**2:.2f} MB")

print("\nData Types")
print(df.dtypes.value_counts())

print("\nDuplicate Rows")
print(df.duplicated().sum())

print("\nFraud Distribution")
print(df["isFraud"].value_counts())

print("\nFraud Percentage")
print(df["isFraud"].value_counts(normalize=True)*100)

print("\nTop 20 Missing Value Columns")

missing = df.isnull().sum().sort_values(ascending=False)

missing_percent = (missing/len(df))*100

report = pd.DataFrame({
    "Missing Values": missing,
    "Percentage": missing_percent
})

print(report.head(20))

report.to_csv(
    f"{RESULT_DIR}/missing_value_report.csv"
)

print("\nMissing value report saved.")
