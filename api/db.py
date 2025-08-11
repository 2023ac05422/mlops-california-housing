import sqlite3
from pathlib import Path
from datetime import datetime
import json

DB_PATH = Path("predictions.sqlite")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS prediction_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            payload TEXT,
            prediction REAL,
            model_version TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def log_prediction(payload: dict, prediction: float, model_version: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO prediction_logs (timestamp, payload, prediction, model_version) 
            VALUES (?, ?, ?, ?)""",
        (
            datetime.utcnow().isoformat(),
            json.dumps(payload),
            float(prediction),
            model_version,
        ),
    )
    conn.commit()
    conn.close()
