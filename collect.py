import subprocess
import time
import requests
import json
import os
import signal
import sys

def get_metrics():
    try:
        r = requests.get("http://localhost:8000/metrics", timeout=5)
        data = r.json()
        keys = ['traffic', 'latency_p50', 'latency_p95', 'latency_p99', 'avg_cost_usd', 
                'total_cost_usd', 'tokens_in_total', 'tokens_out_total', 'error_breakdown', 'quality_avg']
        return {k: data.get(k) for k in keys}
    except Exception as e:
        return {"error": str(e)}

def set_incident(name, enabled):
    action = "enable" if enabled else "disable"
    requests.post(f"http://localhost:8000/incidents/{name}/{action}", timeout=5)

results = {}
# Baseline (assuming uvicorn is running)
subprocess.run(["C:/Users/nmp10/AppData/Local/Programs/Python/Python312/python.exe", "scripts/load_test.py", "--concurrency", "1"])
results["baseline"] = get_metrics()

# rag_slow
set_incident("rag_slow", True)
subprocess.run(["C:/Users/nmp10/AppData/Local/Programs/Python/Python312/python.exe", "scripts/load_test.py", "--concurrency", "1"])
results["rag_slow"] = get_metrics()
set_incident("rag_slow", False)

# tool_fail
set_incident("tool_fail", True)
subprocess.run(["C:/Users/nmp10/AppData/Local/Programs/Python/Python312/python.exe", "scripts/load_test.py", "--concurrency", "1"])
results["tool_fail"] = get_metrics()
set_incident("tool_fail", False)

# cost_spike
set_incident("cost_spike", True)
subprocess.run(["C:/Users/nmp10/AppData/Local/Programs/Python/Python312/python.exe", "scripts/load_test.py", "--concurrency", "1"])
results["cost_spike"] = get_metrics()
set_incident("cost_spike", False)

print(json.dumps(results, indent=2))
