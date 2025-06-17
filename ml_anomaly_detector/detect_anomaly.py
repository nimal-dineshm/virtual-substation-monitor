# ml_anomaly_detector/detect_anomaly.py

import sqlite3
import time
import pandas as pd
from sklearn.ensemble import IsolationForest


def anomaly_detection():
    print("[ML] Anomaly Detection Started")

    while True:
        # Connect to the database and read the last 50 rows
        conn = sqlite3.connect('database/substation_data.db')
        df = pd.read_sql_query("SELECT * FROM readings ORDER BY timestamp DESC LIMIT 50", conn)
        conn.close()

        if df.shape[0] < 10:
            print("[ML] Not enough data yet for detection...")
            time.sleep(5)
            continue

        # Preprocess the data
        df = df.iloc[::-1]  # reverse to chronological
        X = df[['voltage', 'fault']]

        # Fit Isolation Forest and predict anomalies
        model = IsolationForest(contamination=0.1, random_state=42)
        preds = model.fit_predict(X)
        df['anomaly'] = preds

        # Show anomalies
        anomalies = df[df['anomaly'] == -1]
        if not anomalies.empty:
            print("\n[ML] Anomalies Detected:")
            print(anomalies[['timestamp', 'voltage', 'fault']])
        else:
            print("[ML] No anomalies detected")

        time.sleep(10)
