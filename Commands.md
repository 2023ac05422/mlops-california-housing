# Quick Commands

## Setup
```bash
python -m venv venv
./venv/Scripts/Activate.ps1  # Windows PowerShell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Data + DVC
```bash
python -m src.data.make_dataset
dvc init
dvc add data/raw/california_housing.csv
git add .
git commit -m "Add dataset with DVC"
```

## Train & Track
```bash
python -m src.models.train
mlflow ui  # (optional)
```

## Serve
```bash
uvicorn api.main:app --reload --port 8000
```

## Docker
```bash
docker build -t kbatta/california-regressor:latest .
docker run -p 8000:8000 kbatta/california-regressor:latest
```

## CI/CD
- Add repo secrets: `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`
- Push to `main` to trigger workflow.
