# scripts/download_data.py
from pathlib import Path
from sklearn.datasets import fetch_california_housing

OUT_DIR = Path("data/raw")
OUT_DIR.mkdir(parents=True, exist_ok=True)

data = fetch_california_housing(as_frame=True)
df = data.frame  # includes all features + target as "MedHouseVal"
csv_path = OUT_DIR / "california_housing.csv"
df.to_csv(csv_path, index=False)
print(f"Wrote {csv_path.resolve()}")
