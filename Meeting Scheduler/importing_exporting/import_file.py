from datetime import datetime
from tkinter import messagebox

from icalendar import Calendar

from database.manager import DatabaseManager
from validation.importing_validation import validate_meeting_to_import, validate_with_existing_meetings
from validation.importing_validation import verify_events


def transform(events):
    """
    Transforms the events to the format required by the database \n
    Parameters
    ----------
    events: list
        The events to be transformed
    Returns
    -------
    tuple
        The first element is True if the events were transformed successfully, False otherwise
        The second element is the transformed events if the first element is True, error message otherwise
    """
    events_for_db = []
    for event in events:
        event_for_db = {"name": event.get("summary").to_ical().decode('utf-8'), "start_time": event.get("start_time"),
                        "end_time": event.get("end_time")}
        if event_for_db["name"] is None or event_for_db["name"] == "":
            event_for_db["name"] = "Meeting"
        participants = []
        current_time = datetime.now()
        current_timezone = current_time.astimezone().tzinfo
        offset = current_timezone.utcoffset(current_time)
        time_str = event_for_db["start_time"].strftime(
            "%Y-%m-%d %H:%M:%S") + f"+{offset.seconds // 3600:02d}:{(offset.seconds % 3600) // 60:02d}"
        event_for_db["start_time"] = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S%z")
        time_str = event_for_db["end_time"].strftime(
            "%Y-%m-%d %H:%M:%S") + f"+{offset.seconds // 3600:02d}:{(offset.seconds % 3600) // 60:02d}"
        event_for_db["end_time"] = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S%z")
        for attendee in event.get("attendees"):
            parts = attendee.split(";")
            name_part = parts[0]
            name = name_part.split("=")[-1]
            last_name = name.split(" ")[-1]
            first_name = " ".join(name.split(" ")[:-1])
            if len(parts) == 1 or parts[1] == "" or not parts[1].startswith("X-ID"):
                participants.append({"first_name": first_name, "last_name": last_name})
                continue
            id_part = parts[1]
            id = id_part.split("=")[-1]
            try:
                id = int(id)
            except ValueError:
                continue
            participants.append({"first_name": first_name, "last_name": last_name, "id": id})
        event_for_db["participants"] = participants
        events_for_db.append(event_for_db)
        start_date = event_for_db["start_time"].date()
        end_date = event_for_db["end_time"].date()
        start_hour = event_for_db["start_time"].hour
        start_minute = event_for_db["start_time"].minute
        end_hour = event_for_db["end_time"].hour
        end_minute = event_for_db["end_time"].minute
        res, msg = validate_meeting_to_import(start_date, end_date, start_hour, start_minute, end_hour, end_minute,
                                              event_for_db["name"])
        if not res:
            return False, msg
    return True, events_for_db


def add_not_existing_people(participants, all_people, db_manager):
    """
    Adds the people that are not in the database \n
    Parameters
    ----------
    participants: list
        The participants to be added
    all_people: list
        All the people in the database
    db_manager: DatabaseManager
        The database manager
    Returns
    -------
    list
        The new list of participants
    """
    added_people = []
    for participant in participants:
        all_people = db_manager.find_all_persons()
        sorted_ids = sorted([person[0] for person in all_people])
        id = 0
        num = 1
        while id == 0:
            if num not in sorted_ids and num not in added_people:
                id = num
            num += 1
        if "id" in participant.keys():
            added = False
            for person in all_people:
                if person[0] == participant["id"]:
                    if person[1] == participant["first_name"] and person[2] == participant["last_name"]:
                        added = True
                        break
                    else:
                        question = f"There is already a person with ID {person[0]}:\n" \
                                   f"Existing Person: {person[1]} {person[2]}\n" \
                                   f"Person from imported file: {participant['first_name']} {participant['last_name']}"\
                                   "\n" \
                                   "Select yes if you want to add the person from the imported file" \
                                   " with a new ID or no if you want to " \
                                   "replace the existing person."
                        response = messagebox.askquestion("ID Conflict", question, icon='warning')
                        added = True
                        if response == 'yes':
                            res = db_manager.add_person(id, participant["first_name"], participant["last_name"])
                            if not res:
                                messagebox.showerror("Error",
                                                     "There was an error while adding the person to the database!")
                            else:
                                added_people.append(id)
                                participant["id"] = id
                        else:
                            res = db_manager.update_person(participant["id"], participant["first_name"],
                                                           participant["last_name"])
                            if not res:
                                messagebox.showerror("Error",
                                                     "There was an error while updating the person in the database!")
            if not added:
                res = db_manager.add_person(participant["id"], participant["first_name"], participant["last_name"])
                if not res:
                    messagebox.showerror("Error", "There was an error while adding the person to the database!")

        else:
            res = db_manager.add_person(id, participant["first_name"], participant["last_name"])
            if not res:
                messagebox.showerror("Error", "There was an error while adding the person to the database!")
            else:
                participant["id"] = id
                added_people.append(id)
    return participants


def modify_participants(participants):
    """
    Modifies the participants list to be in the format required by the database \n
    Parameters
    ----------
    participants: list
        The participants to be modified
    Returns
    -------
    list
        Modified participants
    """
    modified_participants = []
    for participant in participants:
        modified_participants.append((participant["id"], participant["first_name"], participant["last_name"]))
    return modified_participants


def import_events(file_path):
    """
    Imports the events from the given file
    Parameters
    ----------
    file_path: str
        The path to the file
    Returns
    -------
    tuple
        The first element is True if the events were imported successfully, False otherwise
        The second element is the error message if the first element is False, None otherwise
    """
    if not file_path.endswith(".ics"):
        return False, "The file must be a .ics file"
    try:
        with open(file_path, 'rb') as file:
            cal = Calendar.from_ical(file.read())

            events = []
            for component in cal.walk():
                if component.name == "VEVENT":
                    event = {
                        "uid": component.get('uid'),
                        "summary": component.get('summary', ""),
                        "start_time": component.get('dtstart').dt if component.get('dtstart') else None,
                        "end_time": component.get('dtend').dt if component.get('dtend') else None,
                        "description": component.get('description', ""),
                        "attendees": component.get('ATTENDEE', []),
                    }
                    ok = True
                    if len(event["attendees"]) != 0:
                        for attendee in event["attendees"]:
                            if not attendee.startswith("CN="):
                                ok = False
                                break
                        if not ok:
                            attend = ""
                            for i in event["attendees"]:
                                attend += i
                            event["attendees"] = [attend]
                    events.append(event)
            res, msg = verify_events(events)
            if not res:
                return False, msg
            else:
                res, msg = transform(events)
                if not res:
                    return False, msg
                else:
                    transformed_events = msg
                    db_manager = DatabaseManager()
                    for event in transformed_events:
                        all_people = db_manager.find_all_persons()
                        participants = add_not_existing_people(event["participants"], all_people, db_manager)
                        event["participants"] = participants
                        val, new_ev = validate_with_existing_meetings(event, db_manager)
                        participants = modify_participants(participants)
                        if not val:
                            if new_ev is None:
                                messagebox.showinfo("Info",
                                                    f"The meeting {event['name']} is the same as an existing meeting!"
                                                    " It will not be added to the database!")
                            else:
                                meetings_to_update = new_ev
                                message = f"{event['name']}: There is a meetings with the same name and the same " \
                                          "period of time whose list of participants " \
                                          "includes or is included in this meeting's participants." \
                                          "Choose yes if you want to update the existing meeting" \
                                          " with the new participants or no if you want to keep" \
                                          " the existing version."
                                response = messagebox.askquestion("Common Participants", message, icon='warning')
                                if response == 'yes':
                                    res = db_manager.update_meetings(meetings_to_update, participants)
                                    if not res:
                                        return False, "There was an error while updating the meeting in the database!"
                                elif response == 'no':
                                    continue

                        else:
                            common_participants = new_ev
                            if len(common_participants) == 0:
                                res = db_manager.add_meeting(event["start_time"], event["end_time"], participants,
                                                             event["name"])
                                if not res:
                                    return False, "There was an error while adding a meeting to the database!"
                            else:
                                message = f"The meeting {event['name']} has {len(common_participants)} " \
                                          f"common participants with meetings that happen at the same time:\n"
                                for participant in common_participants:
                                    message += f"{participant[0]} - {participant[1]} {participant[2]}\n"
                                message += "Do you want to add the meeting anyway?"
                                response = messagebox.askquestion("Common Participants", message, icon='warning')
                                if response == 'yes':
                                    res = db_manager.add_meeting(event["start_time"], event["end_time"], participants,
                                                                 event["name"])
                                    if not res:
                                        return False, "There was an error while adding a meeting to the database!"
                                else:
                                    continue
                    return True, None
    except FileNotFoundError:
        return False, "The file does not exist!"
    except ValueError as ve:
        return False, "The file is not a valid .ics file!"
    except Exception as e:
        return False, e
