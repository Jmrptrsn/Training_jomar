from dotenv import load_dotenv
import os
import requests
import base64
import json

# Load .env variables
load_dotenv()

KOHA_API_URL = os.getenv("KOHA_BASE_URL")
USERNAME = os.getenv("KOHA_API_USER")
PASSWORD = os.getenv("KOHA_API_PASSWORD")

# Debug: print values to make sure they loaded correctly
print("KOHA_API_URL:", KOHA_API_URL)
print("USERNAME:", USERNAME)
# print("PASSWORD:", PASSWORD)  # optional, only for testing

# Prepare Basic Auth header
auth_str = f"{USERNAME}:{PASSWORD}"
token = base64.b64encode(auth_str.encode()).decode()
headers = {
    "Authorization": f"Basic {token}",
    "Accept": "application/json"
}

# Try connecting to Koha /biblios endpoint
try:
    response = requests.get(f"{KOHA_API_URL}/biblios", headers=headers, timeout=10)
    print("Status code:", response.status_code)
    try:
        data = response.json()
        print("Response JSON:")
        print(json.dumps(data[:2], indent=2))  # show first 2 records for readability
    except Exception:
        print("Non-JSON response:", response.text)
except Exception as e:
    print("Connection error:", e)
