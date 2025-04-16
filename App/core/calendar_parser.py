import os
from datetime import datetime, timedelta
from icalendar import Calendar
from dateutil.rrule import rrulestr
from dateutil.tz import gettz

CALENDAR_FOLDER = os.path.join(os.getcwd(), "ICS", "calendar")


def _load_ics_events():
    events = []
    ics_files = [f for f in os.listdir(CALENDAR_FOLDER) if f.endswith(".ics")]
    for ics_file in ics_files:
        path = os.path.join(CALENDAR_FOLDER, ics_file)
        with open(path, "r", encoding="utf-8") as f:
            cal = Calendar.from_ical(f.read())
            for component in cal.walk():
                if component.name != "VEVENT":
                    continue
                summary = str(component.get("summary", "No Title"))
                dtstart = component.get("dtstart").dt
                dtend = component.get("dtend").dt
                rrule = component.get("rrule")
                events.append({
                    "summary": summary,
                    "start": dtstart,
                    "end": dtend,
                    "rrule": rrule
                })
    return events


def get_events_for_day(day: datetime):
    tz = gettz("America/New_York")
    start_day = day.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=tz)
    end_day = start_day + timedelta(days=1)
    matched = []

    for event in _load_ics_events():
        start = event["start"]
        end = event["end"]
        rrule = event["rrule"]

        if rrule:
            rule = rrulestr(rrule.to_ical().decode(), dtstart=start)
            occurences = rule.between(start_day, end_day, inc=True)
            for occ in occurences:
                occ_end = occ + (end - start)
                matched.append((event["summary"], occ, occ_end))
        else:
            if start_day <= start < end_day:
                matched.append((event["summary"], start, end))

    return matched


def get_events_today():
    today = datetime.now(gettz("America/New_York"))
    return get_events_for_day(today)


def get_events_this_week():
    today = datetime.now(gettz("America/New_York"))
    end = today + timedelta(days=6 - today.weekday())
    events = []
    for i in range((end - today).days + 1):
        day = today + timedelta(days=i)
        events.extend(get_events_for_day(day))
    return events
