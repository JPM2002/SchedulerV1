import requests

API_KEY = "1050~Cyern2DaVtJCx2uzRWyQtLtXMLe7BJ639JAvw8fe6mBARWavRcUwKmxV2DRYJcYw"
API_URL = "https://psu.instructure.com/api/v1/courses"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

params = {
    "enrollment_state": "active",
    "per_page": 100
}

response = requests.get(API_URL, headers=headers, params=params)

print("Status Code:", response.status_code)
print("Response Headers:", response.headers)
print("Response Text (raw):")
print(repr(response.text))  # show raw format