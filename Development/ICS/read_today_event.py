# File: ICS/read_today_events.py

import os
from datetime import datetime, timedelta
from icalendar import Calendar
from dateutil.rrule import rrulestr
from dateutil.tz import gettz

def get_events_today():
    folder_path = os.path.join(os.getcwd(), "calendar")
    ics_files = [f for f in os.listdir(folder_path) if f.endswith(".ics")]
    if not ics_files:
        print("\U0001F4ED No .ics files found in the calendar folder.")
        return

    now = datetime.now(gettz("America/New_York"))
    start_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_day = start_day + timedelta(days=1)

    events_today = []

    for ics_file in ics_files:
        with open(os.path.join(folder_path, ics_file), "r", encoding="utf-8") as f:
            cal = Calendar.from_ical(f.read())
            for component in cal.walk():
                if component.name != "VEVENT":
                    continue
                summary = str(component.get("summary", "No Title"))
                dtstart = component.get("dtstart").dt
                dtend = component.get("dtend").dt
                if component.get("rrule"):
                    rule = rrulestr(component.get("rrule").to_ical().decode(), dtstart=dtstart)
                    occurences = rule.between(start_day, end_day, inc=True)
                    for occ in occurences:
                        occ_end = occ + (dtend - dtstart)
                        events_today.append((summary, occ, occ_end))
                else:
                    if start_day <= dtstart < end_day:
                        events_today.append((summary, dtstart, dtend))

    if not events_today:
        print("\U0001F389 No events today!")
    else:
        print("\U0001F4C5 Events Today:")
        print("-" * 60)
        for summary, start, end in sorted(events_today, key=lambda x: x[1]):
            print(f"\U0001F552 {start.strftime('%H:%M')} - {end.strftime('%H:%M')} | {summary}")
        print("-" * 60)

# Run
if __name__ == "__main__":
    get_events_today()
