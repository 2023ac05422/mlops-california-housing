import subprocess
import time
import requests

def test_health():
    p = subprocess.Popen(["uvicorn", "api.main:app", "--port", "8001"])
    try:
        time.sleep(2)
        r = requests.get("http://127.0.0.1:8001/health", timeout=5)
        assert r.status_code == 200
    finally:
        p.terminate()
