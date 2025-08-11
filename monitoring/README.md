# Monitoring Add‑On (Prometheus + Grafana)

## Prereqs
- Your API running on host at `http://127.0.0.1:8000` (Dockerfile serves on 0.0.0.0:8000).
- Docker & docker-compose installed.

## Start Prometheus & Grafana
```bash
docker compose up -d
# Prometheus: http://localhost:9090
# Grafana:    http://localhost:3000  (admin / admin)