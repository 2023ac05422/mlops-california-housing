import time
import joblib
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

from api.db import init_db, log_prediction

PRED_COUNT = Counter("pred_requests_total", "Total prediction requests")
PRED_LATENCY = Histogram(
    "pred_request_latency_seconds", "Latency for prediction requests"
)

MODEL_DIR = Path("artifacts/production_model")
PIPELINE_PATH = MODEL_DIR / "pipeline.pkl"
META_PATH = MODEL_DIR / "meta.txt"

app = FastAPI(title="California Housing Regressor", version="1.0.0")


class HousingRecord(BaseModel):
    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    Population: float
    AveOccup: float
    Latitude: float
    Longitude: float

    @field_validator("*")
    @classmethod
    def no_nans(cls, v):
        if v is None:
            raise ValueError("Feature values must be provided")
        return v


def load_model_and_meta():
    if not PIPELINE_PATH.exists():
        raise RuntimeError("Model pipeline not found. Train first.")
    pipeline = joblib.load(PIPELINE_PATH)
    model_version = "unknown"
    if META_PATH.exists():
        model_version = META_PATH.read_text().strip().replace("\n", "; ")
    return pipeline, model_version


@app.on_event("startup")
def _startup():
    init_db()
    app.state.pipeline, app.state.model_version = load_model_and_meta()


@app.get("/health")
def health():
    return {"status": "ok", "model_version": app.state.model_version}


@app.post("/predict")
def predict(rec: HousingRecord):
    PRED_COUNT.inc()
    start = time.time()
    try:
        X = [
            [
                rec.MedInc,
                rec.HouseAge,
                rec.AveRooms,
                rec.AveBedrms,
                rec.Population,
                rec.AveOccup,
                rec.Latitude,
                rec.Longitude,
            ]
        ]
        y_hat = app.state.pipeline.predict(X)[0]
        log_prediction(rec.model_dump(), y_hat, app.state.model_version)
        return {"prediction": float(y_hat)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        PRED_LATENCY.observe(time.time() - start)


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
