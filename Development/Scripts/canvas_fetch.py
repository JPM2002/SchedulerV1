import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()  # Optional, only if using .env

# Use your token or set it in .env as CANVAS_API_KEY
API_KEY = os.getenv("CANVAS_API_KEY", "YOUR_CANVAS_API_KEY")
API_URL = 'https://psu.instructure.com/api/v1/courses?enrollment_state=active'

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

response = requests.get(API_URL, headers=headers)
print(f"Status Code: {response.status_code}")

try:
    courses = response.json()
    if isinstance(courses, str):
        raise ValueError("Received string instead of list")
except Exception as e:
    print("⚠️ Could not parse JSON or data is invalid.")
    print("Raw Response:")
    print(response.text[:500])  # Show first 500 chars
    exit()

# Format dates
def format_date(date_str):
    if date_str:
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ").strftime("%b %d, %Y")
    return "—"

# Display Header
print("\n🎓 My Canvas Courses")
print("-" * 120)
print(f"{'Course Name':<50} {'Code':<30} {'Start':<15} {'End':<15} {'Enrollment'}")
print("-" * 120)

for c in courses:
    try:
        name = c.get("name", "N/A")[:47] + "..." if len(c.get("name", "")) > 50 else c.get("name", "N/A")
        code = c.get("course_code", "N/A")[:28]
        start = format_date(c.get("start_at"))
        end = format_date(c.get("end_at"))
        enrollment = c["enrollments"][0]["enrollment_state"].capitalize() if c.get("enrollments") else "Unknown"
        print(f"{name:<50} {code:<30} {start:<15} {end:<15} {enrollment}")
    except Exception as err:
        print(f"⚠️ Error parsing course: {err}")
        continue

print("-" * 120)

# Optional: Calendar links
print("\n🗓️ Calendar Feeds:")
for c in courses:
    if "calendar" in c:
        print(f"{c['name'][:40]:<40} → {c['calendar']['ics']}")
