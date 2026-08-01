from pathlib import Path
import os
from werkzeug.utils import secure_filename
import psycopg2
from psycopg2 import pool
import time
from prometheus_flask_exporter import PrometheusMetrics
from flask import Flask, render_template, request
import joblib
import pandas as pd
import numpy as np

db_pool = pool.SimpleConnectionPool(
        1, 20,
        host="localhost",
        database="frauddb",
        user="frauduser",
        password="acts"
)

# Loading Trained model
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "xgboost_model.joblib"
model = joblib.load(MODEL_PATH)

X_valid = pd.read_csv(BASE_DIR / "results" / "X_valid.csv")
EXPECTED_COLUMNS = X_valid.columns.tolist()

y_valid = pd.read_csv(BASE_DIR / "results" / "y_valid.csv").squeeze()

encoders = joblib.load(BASE_DIR / "results" / "label_encoders.pkl")

fraud_rows = y_valid[y_valid == 1].index.to_numpy()
legit_rows = y_valid[y_valid == 0].index.to_numpy()

all_predictions = model.predict(X_valid)

correct_fraud_rows = y_valid[(y_valid == 1) & (all_predictions == 1)].index.to_numpy()

correct_legit_rows = y_valid[(y_valid == 0) & (all_predictions == 0)].index.to_numpy()

app = Flask(__name__)
metrics = PrometheusMetrics(app)

UPLOAD_FOLDER = BASE_DIR / "uploads"
UPLOAD_FOLDER.mkdir(exist_ok=True)
app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_csv():

    if "csvfile" not in request.files:
        return "<h2>No file selected</h2>"

    file = request.files["csvfile"]

    if file.filename == "":
        return "<h2>No file selected</h2>"

    filename = secure_filename(file.filename)

    filepath = UPLOAD_FOLDER / filename

    file.save(filepath)

    try:
        df = pd.read_csv(filepath, nrows=5)
    except Exception:
        filepath.unlink(missing_ok=True)
        return """
        <h2>Invalid CSV file.</h2>
        <a href="/">Go Back</a>
        """, 400

    uploaded_columns = df.columns.tolist()
    missing = [
            c for c in EXPECTED_COLUMNS
            if c not in uploaded_columns
    ]
    extra = [
            c for c in uploaded_columns
            if c not in EXPECTED_COLUMNS
    ]

    if missing:
        os.remove(filepath)
        return f"""
        <h2>Invalid Dataset</h2>
        <p><b>Missing Columns:</b></p>
        <pre>{missing}</pre>
        <a href="/">Back</a>
        """, 400


    return f"""
    <h2>CSV Validation Successful</h2>
    <p><b>Filename:</b> {filename}</p>
    <p><b>Rows:</b> {len(df)}</p>
    <p><b>Columns:</b> {len(uploaded_columns)}</p>

    <p style="color:green;">
    Ready for HPC Processing
    </p>
    <a href="/">Back</a>
    """

@app.route("/predict", methods=["POST"])
def predict():
    start = time.time()

    mode = request.form.get("mode","random")
    sample_type = mode.replace("_"," ").title()

    if mode == "fraud":
        if len(correct_fraud_rows):
            idx = int(correct_fraud_rows[0])
        else:
            idx = int(fraud_rows[0])
    
    elif mode == "legitimate":
        if len(correct_legit_rows):
            idx = int(correct_legit_rows[0])
        else:
            idx = int(legit_rows[0])
    
    else:
        idx = 0

    sample = X_valid.loc[[idx]]
    sample_info = sample.iloc[0]
    
    value = sample_info.get("TransactionAmt")
    transaction_amount = float(value) if pd.notna(value) else None

    product = sample_info.get("ProductCD")

    card = sample_info.get("card4")

    try:
        product = encoders["ProductCD"].inverse_transform([int(product)])[0]
    except Exception:
        pass

    try:
        card = encoders["card4"].inverse_transform([int(card)])[0].title()
    except Exception:
        pass

    device = "Unknown"
    browser = "Unknown"

    try:
        prediction = int(model.predict(sample)[0])
        probability = float(model.predict_proba(sample)[0][1])
        
        result = "\U0001F6A8 Fraudulent Transaction" if prediction == 1 else "\u2705 Legitimate Transaction"

        elapsed = float((time.time() - start) * 1000)

        conn = db_pool.getconn()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO prediction_logs(
                        transaction_amount,card_type,device_type,browser,prediction,fraud_probability,
                        response_time_ms) VALUES(%s, %s, %s, %s, %s, %s, %s)""",
                        (
                        float(transaction_amount) if transaction_amount is not None else None,
                        str(card),
                        str(device),
                        str(browser),
                        int(prediction),
                        float(probability),
                        float(elapsed)
                        )

                 )
            conn.commit()
            print("Prediction successfully saved to PostgreSQL")
        
        finally:
            db_pool.putconn(conn)
        
        return f"""
        <h1>{result}</h1>
        <h2>Fraud Probability: {probability:.2%}</h2>

        <hr>

        <h3>Transaction Details</h3>
        <p><b>Sample Type:</b> {sample_type}</p>

        <u1>
        <li><b>Transaction Amount:</b> {transaction_amount}</li>
        <li><b>Product:</b> {product}</li>
        <li><b>Card:</b> {card}</li>
        <li><b>Device:</b> {device}</li>
        <li><b>Browser:</b> {browser}</li>
        <li><b>Prediction Time:</b> {elapsed:.2f} ms</li>
        </u1>

        <hr>
        <a href="/">Check Another Transaction</a>
        """
    except Exception as e: 
        return f"<h2>Prediction Error: {e}</h2><a href="/">Go Back</a>", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)

