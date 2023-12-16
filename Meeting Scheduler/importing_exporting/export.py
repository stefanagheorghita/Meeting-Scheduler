import uuid
from datetime import datetime

from icalendar import Calendar, Event

from database.manager import DatabaseManager


def export(all_meetings, meetings=None):
    """
    Exports the meetings to a .ics file
    :param all_meetings: True if all meetings should be exported, False if only the given meetings should be exported
    :param meetings: the meetings to be exported, None if all meetings should be exported
    :return:
    """
    cal = Calendar()
    cal.add("prodid", "Meeting Scheduler")
    cal.add("version", "2.0")
    db_manager = DatabaseManager()
    if all_meetings:
        meetings = db_manager.get_all_meetings_with_participants()
        for meeting in meetings:
            event = Event()
            timestamp = datetime.now()
            event.add("DTSTAMP", timestamp)
            event.add("UID", f"Meeting-{meeting[0][0]}")
            event.add("SUMMARY", f"Meeting-{meeting[0][0]}")
            start_time_str = meeting[0][1].strftime("%Y-%m-%d %H:%M:%S")
            end_time_str = meeting[0][2].strftime("%Y-%m-%d %H:%M:%S")
            start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
            end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")
            event.add("dtstart", start_time)
            event.add("dtend", end_time)
            start_timezone = start_time.astimezone().tzinfo
            end_timezone = end_time.astimezone().tzinfo
            tz = start_timezone.tzname(start_time)
            tz_end = end_timezone.tzname(end_time)
            event.add('TZID', tz)
            participants_info = "\n".join([f"{participant[1]} {participant[2]}" for participant in meeting[1]])
            event.add("DESCRIPTION", participants_info)
            for participant in meeting[1]:
                full_name = f"{participant[1]} {participant[2]}"
                event.add("ATTENDEE", f"CN={full_name}")
            cal.add_component(event)
    else:
        if meetings is not None:
            for meeting in meetings:
                event = Event()
                timestamp = datetime.now()
                event.add("DTSTAMP", timestamp)
                event.add("UID", f"Meeting-{meeting[0]}")
                event.add("SUMMARY", f"Meeting-{meeting[0]}")
                start_time_str = meeting[1].strftime("%Y-%m-%d %H:%M:%S")
                end_time_str = meeting[2].strftime("%Y-%m-%d %H:%M:%S")
                start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
                end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")
                event.add("dtstart", start_time)
                event.add("dtend", end_time)
                start_timezone = start_time.astimezone().tzinfo
                end_timezone = end_time.astimezone().tzinfo
                tz = start_timezone.tzname(start_time)
                tz_end = end_timezone.tzname(end_time)
                event.add('TZID', tz)
                participants_info = "Participants:\n" + "\n".join(
                    [f"{participant[1]} {participant[2]}" for participant in meeting[3]])
                event.add("DESCRIPTION", participants_info)
                for participant in meeting[3]:
                    full_name = f"{participant[1]} {participant[2]}"
                    event.add("ATTENDEE", f"CN={full_name}")
                cal.add_component(event)
    uid = uuid.uuid4().hex
    if all_meetings:
        file_name = f"calendar_all_meetings_{uid}.ics"
        with open(file_name, "wb") as file:
            file.write(cal.to_ical())
    else:
        file_name = f"calendar_meetings_{uid}.ics"
        with open(file_name, "wb") as file:
            file.write(cal.to_ical())
