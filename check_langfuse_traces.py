import os
import requests
from dotenv import load_dotenv

load_dotenv()

public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
secret_key = os.getenv("LANGFUSE_SECRET_KEY")
base_url = os.getenv("LANGFUSE_BASE_URL") or os.getenv("LANGFUSE_HOST")

if not base_url:
    print("Error: LANGFUSE_BASE_URL or LANGFUSE_HOST not found")
    exit(1)

# Ensure base_url doesn't end with a slash for consistency, then append the path
base_url = base_url.rstrip("/")
url = f"{base_url}/api/public/traces?limit=5"

try:
    response = requests.get(url, auth=(public_key, secret_key))
    print(f"HTTP Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        traces = data.get("data", [])
        print(f"Traces Count: {len(traces)}")
    else:
        print(f"Response Error: {response.text[:300]}")
except Exception as e:
    print(f"Error occurred: {str(e)}")
