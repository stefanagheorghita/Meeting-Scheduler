from datetime import timedelta


def verify_event(event):
    """
    Verifies if the given event is valid
    :param event: The event to be verified.
    :return: True if the event is valid, False otherwise.
    """
    if not event.get("uid"):
        return False
    if not event.get("summary"):
        return False
    if not event.get("start_time"):
        return False
    if not event.get("end_time"):
        return False
    if not event.get("attendees") or (isinstance(event.get("attendees"), list) and all(
            not attendee.strip() for attendee in event.get("attendees"))):
        return False
    return True


def verify_events(events):
    """
    Verifies if the given events are valid
    :param events: The events to be verified.
    :return: True if the events are valid, False otherwise.
    """
    for event in events:
        if not verify_event(event):
            return False, "The event is not valid!"
    return True, None


def validate_meeting_to_import(start_date, end_date, start_hour, start_minute, end_hour, end_minute, name):
    """
    Validates the fields of the meeting
    :param start_date:
    :param end_date:
    :param start_hour:
    :param start_minute:
    :param end_hour:
    :param end_minute:
    :param name:
    :return: (True, None) if the fields are valid, (False, error message) otherwise.
    """
    start_hour = int(start_hour)
    start_minute = int(start_minute)
    end_hour = int(end_hour)
    end_minute = int(end_minute)
    diff_hours = end_hour - start_hour
    diff_time = diff_hours * 60 + end_minute - start_minute
    if start_date > end_date:
        return False, "The start date must be before the end date!"
    if start_date == end_date:
        if start_hour > end_hour:
            return False, "The start hour must be before the end hour!"
        elif start_hour == end_hour:
            if start_minute >= end_minute:
                return False, "The start minute must be before the end minute!"
            elif end_minute - start_minute < 10:
                return False, "There is a meeting which is shorter than 10 minutes!"
        elif diff_time > 5 * 60:
            return False, "There is a meeting that lasts too long!"
    elif (end_date - start_date).days > 1:
        return False, "There is a meeting that lasts too long!"
    elif end_date == start_date + timedelta(days=1):
        diff_hours = 24 - start_hour + end_hour
        diff_time = diff_hours * 60 + end_minute - start_minute
        if diff_time < 10:
            return False, "There is a meeting which is shorter than 10 minutes!"
        elif diff_time > 5 * 60:
            return False, "There is a meeting that lasts too long!"
    return True, None


def validate_same_participants(participants_new, participants_old):
    """
    Validates if the given participants are the same as the participants of the meeting from the database
    :param participants_new: Participants for the meeting to be imported
    :param participants_old: Participants of the meeting from the database
    :return: False if exists at least one participant that is not the same, True otherwise.
    """
    final = 0
    common_participants = []
    for participant in participants_new:
        no = 0
        for participant_old in participants_old:
            if "id" in participant:
                if participant["id"] == participant_old[0] and participant["first_name"] == participant_old[1] and \
                        participant["last_name"] == participant_old[2]:
                    common_participants.append(participant)
                    no += 1
                    break
        if no != 0:
            final += 1
    print(len(participants_new), len(participants_old), final)
    if final == len(participants_new) and len(participants_new) == len(participants_old):
        return True, None
    elif final == len(participants_new):
        return True, "no"
    elif final == len(participants_old):
        return True, "yes"
    return False, common_participants


def meeting_at_same_time(event, existing_meetings):
    """
    Checks if the given event overlaps with any of the existing meetings
    :param event:
    :param existing_meetings:
    :return: the meetings that overlap with the given event if there are any
    """
    comm = []
    for meeting in existing_meetings:
        if meeting[0][1] <= event["start_time"] <= meeting[0][2]:
            comm.append(meeting)
        elif meeting[0][1] <= event["end_time"] <= meeting[0][2]:
            comm.append(meeting)
        elif event["start_time"] <= meeting[0][1] <= event["end_time"]:
            comm.append(meeting)
        elif event["start_time"] <= meeting[0][2] <= event["end_time"]:
            comm.append(meeting)
    return comm


def common_meetings_with_common_participants(event, existing_meetings):
    """
    Checks if the given event overlaps with any of the existing meetings and if there are any common participants
    :param event:
    :param existing_meetings:
    :return: the common participants if there are any, None otherwise.
    """
    common_meetings = meeting_at_same_time(event, existing_meetings)
    common_participants_with_other_meetings = []
    if len(common_meetings) > 0:
        for meeting in common_meetings:
            for participant in meeting[1]:
                for participant_new in event["participants"]:
                    if participant[0] == participant_new["id"] and participant[1] == participant_new["first_name"] and \
                            participant[2] == participant_new["last_name"]:
                        common_participants_with_other_meetings.append(participant)
    common_participants_with_other_meetings = list(set(common_participants_with_other_meetings))
    return common_participants_with_other_meetings


def validate_with_existing_meetings(event, db_manager):
    """
    Validates if the given events overlap with the existing meetings
    :param event: The event to be validated
    :param db_manager: DatabaseManager object
    :return: None if the event is the same as an existing meeting or a list of overlapping meetings if there are an
        """
    existing_meetings = db_manager.get_all_meetings_with_participants()
    name = event["name"]
    start_time = event["start_time"]
    end_time = event["end_time"]
    common_meetings = []
    for meeting in existing_meetings:
        if meeting[0][3] == name:
            if start_time == meeting[0][1] and end_time == meeting[0][2]:
                if validate_same_participants(event["participants"], meeting[1])[0]:
                    if not validate_same_participants(event["participants"], meeting[1])[1]:
                        return False, None
                    else:
                        common_meetings.append(meeting)
    if len(common_meetings) > 0:
        return False, common_meetings
    common_participants_with_meetings_common = common_meetings_with_common_participants(event, existing_meetings)
    return True, common_participants_with_meetings_common
