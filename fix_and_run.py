import subprocess
import time
import requests
import json
import os
import signal
import sys

def call_health():
    try:
        r = requests.get("http://localhost:8000/health", timeout=5)
        return r.status_code == 200
    except:
        return False

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
    try:
        action = "enable" if enabled else "disable"
        requests.post(f"http://localhost:8000/incidents/{name}/{action}", timeout=5)
    except:
        pass

def run_load_test():
    subprocess.run(["C:/Users/nmp10/AppData/Local/Programs/Python/Python312/python.exe", "scripts/load_test.py", "--concurrency", "1"], 
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# CLEANUP OLD PROCESSES
subprocess.run(["taskkill", "/F", "/IM", "python.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(2)

# Start uvicorn
proc = subprocess.Popen(["C:/Users/nmp10/AppData/Local/Programs/Python/Python312/python.exe", "-m", "uvicorn", "app.main:app", "--port", "8000"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

try:
    # Wait for health
    connected = False
    for i in range(20):
        if call_health():
            connected = True
            break
        time.sleep(1)
    
    if not connected:
        sys.exit(1)

    results = {}
    for incident in ["rag_slow", "tool_fail", "cost_spike"]:
        set_incident(incident, False)

    run_load_test()
    results["baseline"] = get_metrics()

    for incident in ["rag_slow", "tool_fail", "cost_spike"]:
        set_incident(incident, True)
        run_load_test()
        results[incident] = get_metrics()
        set_incident(incident, False)

    with open("results.json", "w") as f:
        json.dump(results, f)

finally:
    proc.terminate()
