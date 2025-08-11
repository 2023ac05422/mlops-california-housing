# California Housing — End-to-End MLOps

This repo contains a minimal but complete MLOps pipeline for the **California Housing** regression dataset:

- Data versioning with DVC
- MLflow experiment tracking
- Two models (Linear Regression, Decision Tree) with best-model export
- FastAPI service with Pydantic validation
- Docker image
- GitHub Actions CI (lint, test, build & push Docker)
- Basic monitoring via Prometheus `/metrics` and SQLite request logging

See `SUMMARY.md` for a 1-page architecture overview and `Commands.md` for quick commands.
