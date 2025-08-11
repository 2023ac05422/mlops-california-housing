#!/usr/bin/env bash
set -e
if [ data/raw/california_housing.csv -nt artifacts/production_model/pipeline.pkl ]; then
  echo "New data detected. Retraining..."
  python -m src.models.train
else
  echo "Model is up-to-date."
fi
