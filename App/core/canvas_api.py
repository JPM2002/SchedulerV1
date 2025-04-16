import requests
import pytz
from datetime import datetime
from dateutil import parser
from core.config import load_api_key

BASE_URL = "https://psu.instructure.com/api/v1"
eastern = pytz.timezone("America/New_York")


def get_headers():
    api_key = load_api_key()
    if not api_key:
        print("❌ No API key found. Please add one using the menu.")
        return None
    return {"Authorization": f"Bearer {api_key}"}


def get_courses():
    headers = get_headers()
    if not headers:
        return []

    url = f"{BASE_URL}/courses?enrollment_state=active&per_page=100"
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else []


def get_assignments_due_today():
    headers = get_headers()
    if not headers:
        return []

    today = datetime.now(eastern).date()
    results = []

    for course in get_courses():
        course_name = course.get("name", "N/A")
        course_id = course.get("id")
        if not course_id:
            continue

        url = f"{BASE_URL}/courses/{course_id}/assignments?per_page=100"
        response = requests.get(url, headers=headers)
        assignments = response.json() if response.status_code == 200 else []

        for a in assignments:
            due = a.get("due_at")
            if not due:
                continue

            due_dt = parser.isoparse(due).astimezone(eastern)
            if due_dt.date() == today:
                results.append({
                    "name": a["name"],
                    "due_time": due_dt.strftime("%I:%M %p").lstrip("0"),
                    "course": course_name,
                    "link": a["html_url"]
                })

    return results


def print_assignments_due_today():
    assignments = get_assignments_due_today()

    print("📌 Assignments Due Today")
    print("-" * 80)

    if not assignments:
        print("🎉 No assignments due today! Enjoy your day 🎈")
        return

    for item in assignments:
        print(f"📝 {item['name'][:45]:<45} ({item['due_time']})")
        print(f"   📚 {item['course']}")
        print(f"   🔗 {item['link']}")
        print("-" * 80)
