import os
import argparse
import joblib
import pandas as pd
import xgboost as xgb
from sklearn.metrics import (accuracy_score,precision_score,recall_score,f1_score,roc_auc_score,confusion_matrix,classification_report)

parser = argparse.ArgumentParser()

parser.add_argument("--depth", type=int, default=8)
parser.add_argument("--lr", type=float, default=0.05)

args = parser.parse_args()

RESULT_DIR = "/home/project/FraudDetection/results"
MODEL_DIR = "/home/project/FraudDetection/models"
os.makedirs(MODEL_DIR, exist_ok=True)

print("="*70)
print("Loading Training Data...")
print("="*70)

X_train = pd.read_csv(f"{RESULT_DIR}/X_train.csv")
X_valid = pd.read_csv(f"{RESULT_DIR}/X_valid.csv")

y_train = pd.read_csv(f"{RESULT_DIR}/y_train.csv").squeeze()
y_valid = pd.read_csv(f"{RESULT_DIR}/y_valid.csv").squeeze()

print("Training Shape :", X_train.shape)
print("Validation Shape :", X_valid.shape)

print("\nTraining XGBoost Model...")

model = xgb.XGBClassifier(n_estimators=300,max_depth=args.depth,learning_rate=args.lr,subsample=0.8,colsample_bytree=0.8,objective="binary:logistic",eval_metric="logloss",random_state=42,n_jobs=-1)

model.fit(X_train, y_train)

print("Training Completed.")
print("\nEvaluating Model...")

pred = model.predict(X_valid)
prob = model.predict_proba(X_valid)[:,1]

accuracy = accuracy_score(y_valid,pred)
precision = precision_score(y_valid,pred)
recall = recall_score(y_valid,pred)
f1 = f1_score(y_valid,pred)
roc = roc_auc_score(y_valid,prob)

print("\nAccuracy :",accuracy)
print("Precision:",precision)
print("Recall :",recall)
print("F1 :",f1)
print("ROC-AUC :",roc)

print("\nConfusion Matrix")

print(confusion_matrix(y_valid,pred))

print("\nClassification Report")

print(classification_report(y_valid,pred))

model_name = f"xgb_depth{args.depth}_lr{args.lr}.joblib"
joblib.dump(
        model,
        f"{MODEL_DIR}/{model_name}"
)

print(f"Saved {model_name}")

print("\nModel Saved Successfully.")


