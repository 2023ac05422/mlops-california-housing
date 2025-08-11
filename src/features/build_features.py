from dataclasses import dataclass
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

FEATURES = [
    "MedInc",
    "HouseAge",
    "AveRooms",
    "AveBedrms",
    "Population",
    "AveOccup",
    "Latitude",
    "Longitude",
]
TARGET = "MedHouseVal"


@dataclass
class SplitData:
    X_train: pd.DataFrame
    X_test: pd.DataFrame
    y_train: pd.Series
    y_test: pd.Series


def train_test_split_df(
    df: pd.DataFrame, test_size: float = 0.2, random_state: int = 42
) -> SplitData:
    X = df[FEATURES]
    y = df[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    return SplitData(X_train, X_test, y_train, y_test)


def build_preprocessor() -> ColumnTransformer:
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), FEATURES),
        ],
        remainder="drop",
    )


def build_pipeline(estimator) -> Pipeline:
    return Pipeline(steps=[("preprocess", build_preprocessor()), ("model", estimator)])
