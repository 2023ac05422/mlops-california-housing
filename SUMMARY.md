# MLOps Pipeline — California Housing (Regression)

## Overview
End-to-end MLOps pipeline using Git, DVC, MLflow, FastAPI, Docker, and GitHub Actions.
Dataset: California Housing (sklearn). Target: `MedHouseVal`.

## Architecture
1. **Data Versioning**: `src/data/make_dataset.py` fetches dataset to `data/raw/`. Tracked by DVC.
2. **Model Dev & Tracking**:
   - Models: `LinearRegression`, `DecisionTreeRegressor`.
   - MLflow logs params/metrics/artifacts; best by RMSE exported to `artifacts/production_model/pipeline.pkl`.
3. **Serving**:
   - FastAPI (`api/main.py`): `/predict` (Pydantic validation), `/health`, `/metrics` (Prometheus).
   - Logs to SQLite (`api/db.py`).
4. **Containerization**:
   - Dockerfile builds image, runs `uvicorn`.
5. **CI/CD**:
   - GitHub Actions: lint, test, build, push to Docker Hub on `main`.
6. **Monitoring**:
   - Request counter & latency histogram at `/metrics`.
   - Request+prediction audit logs in `predictions.sqlite`.

## How to Run (local)
```bash
python -m venv venv
./venv/Scripts/activate  # Windows PowerShell
python -m pip install --upgrade pip
pip install -r requirements.txt

python -m src.data.make_dataset
dvc init
dvc add data/raw/california_housing.csv

python -m src.models.train

uvicorn api.main:app --reload --port 8000
# test
curl -X POST "http://127.0.0.1:8000/predict" -H "Content-Type: application/json" -d '{"MedInc":8.3,"HouseAge":41.0,"AveRooms":5.9,"AveBedrms":1.1,"Population":980.0,"AveOccup":2.7,"Latitude":34.2,"Longitude":-118.3}'
```

## Docker
```bash
docker build -t <dockerhub>/california-regressor:latest .
docker run -p 8000:8000 <dockerhub>/california-regressor:latest
```

## Links (fill after you push)
- GitHub: <repo>
- Docker Hub: <image>
- MLflow UI (optional): http://127.0.0.1:5000
