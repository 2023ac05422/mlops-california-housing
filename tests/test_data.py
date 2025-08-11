from pathlib import Path
import pandas as pd


def test_raw_data_exists():
    assert Path("data/raw/california_housing.csv").exists()


def test_csv_has_columns():
    df = pd.read_csv("data/raw/california_housing.csv")
    expected = {
        "MedInc",
        "HouseAge",
        "AveRooms",
        "AveBedrms",
        "Population",
        "AveOccup",
        "Latitude",
        "Longitude",
        "MedHouseVal",
    }
    assert expected.issubset(set(df.columns))
