from pathlib import Path
import pandas as pd

def ensure_dir(path: str | Path) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)

def save_csv(df: pd.DataFrame, path: str | Path) -> None:
    ensure_dir(Path(path).parent)
    df.to_csv(path, index=False)

def load_csv(path: str | Path) -> pd.DataFrame:
    return pd.read_csv(path)
