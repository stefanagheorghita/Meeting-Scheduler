from datetime import timedelta, datetime


def validate_meeting_search(start_date, end_date, start_hour, start_minute, end_hour, end_minute):
    """
    Validates the fields of the meeting \n
    Parameters
    ----------
    start_date: datetime.datetime
        The start date of the meeting
    end_date: datetime.datetime
        The end date of the meeting
    start_hour: str
        The start hour of the meeting
    start_minute: str
        The start minute of the meeting
    end_hour: str
        The end hour of the meeting
    end_minute: str
        The end minute of the meeting
    Returns
    -------
    tuple
        The first element is True if the meeting is valid, False otherwise
        The second element is None if the meeting is valid, an error message otherwise
    """
    if end_date < start_date:
        return False, "The start date must be before the end date!"
    elif end_date == start_date:
        if end_hour < start_hour:
            return False, "The start hour must be before the end hour!"
        elif end_hour == start_hour:
            if end_minute <= start_minute:
                return False, "The start minute must be before the end minute!"
    return True, None


def validate_meeting_data(start_date, end_date, start_hour, start_minute, end_hour, end_minute, name):
    """
    Validates the fields of the meeting \n
    Parameters
    ----------
    start_date: datetime.datetime
        The start date of the meeting
    end_date: datetime.datetime
        The end date of the meeting
    start_hour: str
        The start hour of the meeting
    start_minute: str
        The start minute of the meeting
    end_hour: str
        The end hour of the meeting
    end_minute: str
        The end minute of the meeting
    name: str
        The name of the meeting
    Returns
    -------
    tuple
        The first element is True if the meeting is valid, False otherwise
        The second element is None if the meeting is valid, an error message otherwise
    """
    start_hour = int(start_hour)
    start_minute = int(start_minute)
    end_hour = int(end_hour)
    end_minute = int(end_minute)
    current_time = datetime.now()
    if name == "":
        return False, "Please introduce a name for the meeting!"
    if start_date < current_time.date():
        return False, "The start date must be after the current date!"
    elif start_date == current_time.date():
        hour_diff = start_hour - current_time.hour
        diff = hour_diff * 60 + start_minute - current_time.minute
        if diff < 0:
            return False, "You can't add a meeting that starts in the past!"
        elif diff < 60:
            return False, "You can't add a meeting that starts in less than an hour!"
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
                return False, "The meeting must last at least 10 minutes!"
        elif diff_time > 5 * 60:
            return False, "The meeting lasts too long!"
    elif (end_date - start_date).days > 1:
        return False, "The meeting lasts too long!"
    elif end_date == start_date + timedelta(days=1):
        diff_hours = 24 - start_hour + end_hour
        diff_time = diff_hours * 60 + end_minute - start_minute
        if diff_time < 10:
            return False, "The meeting must last at least 10 minutes!"
        elif diff_time > 5 * 60:
            return False, "The meeting lasts too long!"
    return True, None
