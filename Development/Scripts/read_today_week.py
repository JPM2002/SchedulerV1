# File: ICS/read_today_event.py

import os
from datetime import datetime, timedelta
from ics import Calendar
from zoneinfo import ZoneInfo

# Define today's and this week's time window
now = datetime.now(ZoneInfo("America/New_York"))
today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
today_end = today_start + timedelta(days=1)
week_end = today_start + timedelta(days=7)


def parse_ics_events(path):
    with open(path, 'r', encoding='utf-8') as file:
        calendar = Calendar(file.read())

    events_today = []
    events_this_week = []

    for event in calendar.timeline:
        if not event.begin:
            continue
        event_start = event.begin.astimezone(ZoneInfo("America/New_York"))
        event_end = event.end.astimezone(ZoneInfo("America/New_York")) if event.end else event_start + timedelta(hours=1)

        if today_start <= event_start < today_end:
            events_today.append((event.name, event_start.time(), event_end.time()))
        if today_start <= event_start < week_end:
            events_this_week.append((event.name, event_start.strftime('%a %H:%M'), event_end.strftime('%H:%M')))

    return events_today, events_this_week


def show_today_events(events):
    if not events:
        print("🎉 No events today!")
    else:
        print("📅 Events for Today:")
        print("-" * 60)
        for name, start, end in sorted(events, key=lambda x: x[1]):
            print(f"🕒 {start.strftime('%H:%M')} - {end.strftime('%H:%M')} | {name}")
        print("-" * 60)


def show_week_events(events):
    if not events:
        print("📭 No events scheduled for this week.")
    else:
        print("📆 Events for This Week:")
        print("-" * 60)
        for name, start, end in sorted(events, key=lambda x: x[1]):
            print(f"🗓️  {start} - {end} | {name}")
        print("-" * 60)


# Entry point
def main():
    base_folder = os.path.join(os.getcwd(), "calendar")
    os.makedirs(base_folder, exist_ok=True)

    ics_files = [f for f in os.listdir(base_folder) if f.endswith(".ics")]
    if not ics_files:
        print("📭 No .ics file found in 'calendar'")
        return

    full_path = os.path.join(base_folder, ics_files[0])
    events_today, events_week = parse_ics_events(full_path)

    show_today_events(events_today)
    print("\n")
    show_week_events(events_week)


if __name__ == "__main__":
    main()
