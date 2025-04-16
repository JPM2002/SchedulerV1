import requests
import os
from dotenv import load_dotenv
from datetime import datetime
from dateutil import parser
import pytz

load_dotenv()
API_KEY = os.getenv("CANVAS_API_KEY")
BASE_URL = "https://psu.instructure.com/api/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# Convert UTC to Eastern Time
utc = pytz.utc
eastern = pytz.timezone("America/New_York")
today = datetime.now(eastern).date()

def get_courses():
    url = f"{BASE_URL}/courses?enrollment_state=active&per_page=100"
    response = requests.get(url, headers=HEADERS)
    return response.json() if response.status_code == 200 else []

def get_assignments(course_id):
    url = f"{BASE_URL}/courses/{course_id}/assignments?per_page=100"
    response = requests.get(url, headers=HEADERS)
    return response.json() if response.status_code == 200 else []

print("📌 Assignments Due Today")
print("-" * 80)
found = False

for course in get_courses():
    course_name = course.get("name", "N/A")
    course_id = course.get("id")
    
    assignments = get_assignments(course_id)
    for a in assignments:
        due = a.get("due_at")
        if not due:
            continue

        # Parse and convert to local time
        due_dt = parser.isoparse(due).astimezone(eastern)
        if due_dt.date() == today:
            found = True
            time_str = due_dt.strftime("%I:%M %p").lstrip("0")
            print(f"📝 {a['name'][:45]:<45} ({time_str})")
            print(f"   📚 {course_name}")
            print(f"   🔗 {a['html_url']}")
            print("-" * 80)

if not found:
    print("🎉 No assignments due today! Enjoy your day 🎈")
