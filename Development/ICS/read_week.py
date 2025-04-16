import os
from datetime import datetime, timedelta
from icalendar import Calendar, Event
from dateutil.rrule import rrulestr
from dateutil.tz import gettz

def get_this_week_events():
    folder_path = os.path.join(os.getcwd(), "calendar")

    ics_files = [f for f in os.listdir(folder_path) if f.endswith(".ics")]
    if not ics_files:
        print("📭 No .ics files found in the calendar folder.")
        return

    this_week_events = []

    now = datetime.now(gettz("America/New_York"))
    start_week = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_week = start_week + timedelta(days=6)

    for ics_file in ics_files:
        file_path = os.path.join(folder_path, ics_file)
        with open(file_path, "r", encoding="utf-8") as f:
            cal = Calendar.from_ical(f.read())

            for component in cal.walk():
                if component.name != "VEVENT":
                    continue

                summary = str(component.get("summary", "No Title"))
                dtstart = component.get("dtstart").dt
                dtend = component.get("dtend").dt

                # Handle recurring events
                if component.get("rrule"):
                    rule = rrulestr(component.get("rrule").to_ical().decode(), dtstart=dtstart)
                    occurences = rule.between(start_week, end_week, inc=True)
                    for occ in occurences:
                        occ_end = occ + (dtend - dtstart)
                        this_week_events.append((summary, occ, occ_end))
                else:
                    if start_week <= dtstart <= end_week:
                        this_week_events.append((summary, dtstart, dtend))

    if not this_week_events:
        print("📭 No events scheduled for this week.")
    else:
        print("📅 Events This Week:")
        print("-" * 60)
        for summary, start, end in sorted(this_week_events, key=lambda x: x[1]):
            print(f"{start.strftime('%a %b %d')} | {start.strftime('%H:%M')} - {end.strftime('%H:%M')} | {summary}")
        print("-" * 60)

# Run
get_this_week_events()
