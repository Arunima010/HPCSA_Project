import io
import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL Connection
engine = create_engine(
    "postgresql+psycopg2://frauduser:acts@localhost/frauddb"
)

print("Loading cleaned dataset...")
df = pd.read_csv("/home/project/FraudDetection/results/cleaned_dataset.csv")
print("Dataset Shape:", df.shape)

print("Uploading data to PostgreSQL using fast COPY...")

# 1. Create the empty table structure (fast)
df.head(0).to_sql(
    "fraud_transactions",
    engine,
    if_exists="replace",
    index=False
)

# 2. Get raw psycopg2 connection for COPY operation
conn = engine.raw_connection()
try:
    cursor = conn.cursor()
   
    # Stream data to in-memory CSV buffer
    sio = io.StringIO()
    df.to_csv(sio, index=False, header=False)
    sio.seek(0)
   
    # Bulk import into PostgreSQL
    copy_sql = "COPY fraud_transactions FROM STDIN WITH CSV DELIMITER ','"
    cursor.copy_expert(copy_sql, sio)
   
    conn.commit()
    cursor.close()
    print("Upload Complete!")
except Exception as e:
    conn.rollback()  # Resets any failed transaction state safely
    print("Error during upload:", e)
finally:
    conn.close()
