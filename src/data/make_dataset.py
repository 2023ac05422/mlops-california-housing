from pathlib import Path
from sklearn.datasets import fetch_california_housing
from src.utils.io import save_csv

RAW_CSV = Path("data/raw/california_housing.csv")

if __name__ == "__main__":
    data = fetch_california_housing(as_frame=True)
    df = data.frame.copy()
    save_csv(df, RAW_CSV)
    print(f"Saved: {RAW_CSV.absolute()}")
