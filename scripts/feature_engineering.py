import pandas as pd
import os
from sklearn.impute import SimpleImputer

DATA_DIR = "/home/project/FraudDetection/results"
RESULT_DIR = "/home/project/FraudDetection/results"
os.makedirs(RESULT_DIR, exist_ok=True)

print("="*70)
print("Loading merged dataset...")
print("="*70)

df = pd.read_csv(f"{DATA_DIR}/merged_dataset.csv")
print("Original Shape:", df.shape)

# -------------------------------------------------
# Drop columns having more than 90% missing values
# -------------------------------------------------

threshold = len(df) * 0.90
df = df.dropna(axis=1, thresh=threshold)
print("After dropping sparse columns:", df.shape)

# -------------------------------------------------
# Separate numeric and categorical columns
# -------------------------------------------------

numeric_cols = df.select_dtypes(include=["int64","float64"]).columns

categorical_cols = df.select_dtypes(include=["object"]).columns

print("Numeric Columns:", len(numeric_cols))
print("Categorical Columns:", len(categorical_cols))

# -------------------------------------------------
# Fill numeric missing values with median
# -------------------------------------------------

num_imputer = SimpleImputer(strategy="median")

df[numeric_cols] = num_imputer.fit_transform(df[numeric_cols])

# -------------------------------------------------
# Fill categorical missing values with most frequent
# -------------------------------------------------

cat_imputer = SimpleImputer(strategy="most_frequent")

df[categorical_cols] = cat_imputer.fit_transform(df[categorical_cols])

print("\nRemaining Missing Values")
print(df.isnull().sum().sum())

# -------------------------------------------------
# Save cleaned dataset
# -------------------------------------------------

df.to_csv(f"{RESULT_DIR}/cleaned_dataset.csv",index=False)

print("\nSaved cleaned_dataset.csv")
print("Final Shape:", df.shape)
