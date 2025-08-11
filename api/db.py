import json
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path("predictions.sqlite")


def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
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


def log_prediction(payload: dict, prediction: float, model_version: str) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO prediction_logs (timestamp, payload, prediction, model_version)
            VALUES (?, ?, ?, ?)
            """,
            (
                datetime.utcnow().isoformat(),
                json.dumps(payload),
                float(prediction),
                model_version,
            ),
        )
        conn.commit()
