#!/usr/bin/env bash
set -e
IMAGE=${1:-kbatta/california-regressor:latest}
docker pull $IMAGE || true
docker stop cali || true
docker rm cali || true
docker run -d --name cali -p 8000:8000 $IMAGE
echo "API running at http://localhost:8000"
