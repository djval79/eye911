"""
NHTSA API Key Request Submission Script
"""
import requests

request_data = {
    "organization": "NOVUMSOLVO",
    "contact_email": "valentine@novumsolvo.co.uk",
    "use_case": "Traffic safety monitoring application",
    "expected_volume": "<1000 requests/day"
}

print("Submitting NHTSA API key request...")
try:
    response = requests.post(
        "https://crashviewer.nhtsa.dot.gov/CrashAPI/key_request",
        json=request_data,
        timeout=10
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error submitting request: {str(e)}")
