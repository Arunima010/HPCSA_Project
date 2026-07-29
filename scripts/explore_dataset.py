import pandas as pd

# Dataset location
DATA_PATH = "/home/project/FraudDetection/data"
print("Loading datasets...")

train_transaction = pd.read_csv(f"{DATA_PATH}/train_transaction.csv")

train_identity = pd.read_csv(f"{DATA_PATH}/train_identity.csv")

print("\nTrain Transaction Shape:")
print(train_transaction.shape)

print("\nTrain Identity Shape:")
print(train_identity.shape)

print("\nTransaction Columns:")
print(train_transaction.columns.tolist()[:20])

print("\nIdentity Columns:")
print(train_identity.columns.tolist())

print("\nTransaction Head:")
print(train_transaction.head())

print("\nIdentity Head:")
print(train_identity.head())
