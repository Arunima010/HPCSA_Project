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
MODEL_PATH = "/home/project/FraudDetection/models/xgboost_model.joblib"
model = joblib.load(MODEL_PATH)

X_valid = pd.read_csv("/home/project/FraudDetection/results/X_valid.csv")
y_valid = pd.read_csv("/home/project/FraudDetection/results/y_valid.csv").squeeze()

fraud_rows = y_valid[y_valid == 1].index.to_numpy()
legit_rows = y_valid[y_valid == 0].index.to_numpy()

app = Flask(__name__)
metrics = PrometheusMetrics(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    start = time.time()

    try:
        amount = float(request.form.get("amount", 0))
        if amount <= 0:
            return """
            <h2>Transaction amount must be greater than zero.</h2>
            <a href="/">Go Back</a>
            """, 400
    except ValueError:
        return """
        <h2>Please enter a valid numeric amount.</h2>
        <a href='/'>Go Back</a>
        """,400
    card = request.form.get("card","unknown")
    device = request.form.get("device","unknown")
    browser = request.form.get("browser","unknown")
    mode = request.form.get("mode","random")

    if mode == "fraud":
        idx = np.random.choice(fraud_rows)
    
    elif mode == "legitimate":
        idx = np.random.choice(legit_rows)
    
    else:
        idx = np.random.choice(X_valid.index.to_numpy())

    sample = X_valid.loc[[idx]]

    try:
        prediction = int(model.predict(sample)[0])
        probability = float(model.predict_proba(sample)[0][1])
        
        result = "\U0001F6A8 Fraudulent Transaction" if prediction == 1 else "\u2705 Legitimate Transaction"

        elapsed = (time.time() - start) * 1000

        conn = db_pool.getconn()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO prediction_logs(
                        transaction_amount,card_type,device_type,browser,prediction,fraud_probability,
                        response_time_ms) VALUES(%s, %s, %s, %s, %s, %s, %s)""",
                        (amount,card,device,browser,prediction,probability,elapsed)

                 )
            conn.commit()
        
        finally:
            db_pool.putconn(conn)
        
        return f"""
        <h1>{result}</h1>
        <h2>Fraud Probability: {probability:.2%}</h2>
        <br>
        <a href="/">Check Another Transaction</a>
        """
    except Exception as e: 
        return f"<h2>Prediction Error: {e}</h2><a href="/">Go Back</a>", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)

