from pathlib import Path
import joblib
import mlflow
import mlflow.sklearn
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor

from src.utils.io import load_csv, ensure_dir
from src.features.build_features import train_test_split_df, build_pipeline
from src.utils.metrics import regression_metrics

RAW_CSV = Path("data/raw/california_housing.csv")
PROD_DIR = Path("artifacts/production_model")
EXPERIMENT_NAME = "california-housing-regression"
MODEL_NAME = "california-regressor"


def train_and_log(model_name: str, est, X_train, y_train, X_test, y_test):
    with mlflow.start_run(run_name=model_name):
        pipe = build_pipeline(est)
        pipe.fit(X_train, y_train)

        preds = pipe.predict(X_test)
        m = regression_metrics(y_test, preds)

        if hasattr(est, "get_params"):
            mlflow.log_params(est.get_params())
        mlflow.log_metrics(m)

        mlflow.sklearn.log_model(
            pipe, artifact_path="model", registered_model_name=None
        )
        mlflow.set_tag("model_name", model_name)

        run_id = mlflow.active_run().info.run_id
        return m, run_id


if __name__ == "__main__":
    mlflow.set_experiment(EXPERIMENT_NAME)

    df = load_csv(RAW_CSV)
    split = train_test_split_df(df)

    candidates = [
        ("LinearRegression", LinearRegression()),
        ("DecisionTreeRegressor", DecisionTreeRegressor(random_state=42, max_depth=10)),
    ]

    results = []
    for name, est in candidates:
        metrics, run_id = train_and_log(
            name, est, split.X_train, split.y_train, split.X_test, split.y_test
        )
        results.append((name, metrics["rmse"], run_id, metrics))

    results.sort(key=lambda x: x[1])
    best_name, best_rmse, best_run, best_metrics = results[0]
    print(f"Best: {best_name} (RMSE={best_rmse:.4f}) run_id={best_run}")

    client = mlflow.tracking.MlflowClient()
    _ = client.list_artifacts(best_run, "model")
    local_dir = Path("artifacts/_tmp_download")
    ensure_dir(local_dir)
    dst = client.download_artifacts(best_run, "model", str(local_dir))

    ensure_dir(PROD_DIR)
    joblib.dump(joblib.load(Path(dst) / "model.pkl"), PROD_DIR / "pipeline.pkl")

    with open(PROD_DIR / "meta.txt", "w", encoding="utf-8") as f:
        f.write(f"best_run_id={best_run}\nmodel={best_name}\nrmse={best_rmse}\n")

    print("Exported production model to artifacts/production_model/pipeline.pkl")
