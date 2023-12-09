from database.manager import DatabaseManager


def format_name(name):
    """
    It formats the name to have the first letter of each word capitalized.
    :param name: name to be formatted
    :return: formatted name
    """
    new_name = name.strip()
    new_name = new_name.lower()
    formatted = ""
    formatted += new_name[0].upper()
    for i in range(1, len(new_name)):
        if new_name[i - 1] == "-" or new_name[i - 1] == "'" or new_name[i - 1] == " ":
            formatted += new_name[i].upper()
        else:
            formatted += new_name[i]
    parts = [part for part in formatted.replace('-', ' ').split() if part.strip()]
    formatted_name = '-'.join(parts)

    parts = [part for part in formatted_name.replace("'", ' ').split() if part.strip()]
    formatted_name = "'".join(parts)
    return formatted_name


def validate_consecutive(name, sep):
    """
    Validates that the name doesn't contain consecutive separators.
    :param name: name to be validated
    :param sep: separator
    :return: True if the name is valid, False otherwise.
    """
    parts = name.split(sep)
    for part in parts:
        if all(char.isspace() for char in part):
            return False
    return True


def validate_name(name, flag):
    """
    Validates the basic rules for a name. The name must contain only letters, spaces, dashes or apostrophes.
    :param name: name to be validated
    :param flag: "first" or "last"
    :return: (True, None) if the name is valid, (False, error message) otherwise.
    """
    name = name.strip()
    n_chr = [c for c in name if c.isalpha() or c == " " or c == "-" or c == "'"]
    name = name.strip()
    if name.startswith("-") or name.endswith("-") or name.startswith("'") or name.endswith("'"):
        return False, f"Invalid format for {flag} name!"
    if len(n_chr) != len(name):
        return False, f"{flag[0].upper()+flag[1:]} name has some invalid symbols!"
    if not validate_consecutive(name, "-"):
        return False, f"Invalid format for {flag} name!"
    if not validate_consecutive(name, "'"):
        return False, f"Invalid format for {flag} name!"
    return True, None


def add_person_validation(id, first_name, last_name):
    """
    Validates the fields of the add person window and adds the person to the database
    :param id: id of the person
    :param first_name: First name of the person
    :param last_name: Last name of the person
    :return: (True, message) if the fields are valid, (False, error message) otherwise.
    """
    message = None
    if id == "" or first_name == "" or last_name == "":
        return False, "All fields must be filled!"
    if not id.isdigit():
        return False, "Id must be a number!"
    if int(id) <= 0 or int(id) > 2147483647:
        return False, "The id is not within the limits!"
    result, msg = validate_name(first_name, "first")
    result2, msg2 = validate_name(last_name, "last")
    if not result or not result2:
        if msg is not None:
            return False, msg
        else:
            return False, msg2
    db_manager = DatabaseManager()
    id = int(id)
    if not db_manager.search_id_db(id):
        return False, "There is already a person in the database with the given id!"
    first_name = first_name.strip()
    last_name = last_name.strip()
    first_name_formatted = format_name(first_name)
    last_name_formatted = format_name(last_name)
    if first_name_formatted[1:] != first_name[1:] or last_name_formatted[1:] != last_name[1:]:
        message = first_name_formatted + "!!" + last_name_formatted
    else:
        if first_name_formatted[0] != first_name[0] or last_name_formatted[0] != last_name[0]:
            message = "The person was added to the database as " + first_name_formatted + " " + last_name_formatted + \
                      "!"
        first_name = first_name_formatted
        last_name = last_name_formatted
    if message is None:
        if not db_manager.add_person(id, first_name, last_name):
            return False, "An error occurred while adding the person to the database!"
    return True, message


def add_person_confirmation(id, first_name, last_name):
    """
    Adds the person to the database, for the case where the user is asked which format is correct.
    :param id: id of the person
    :param first_name: First name of the person
    :param last_name: Last name of the person
    :return:
    """
    db_manager = DatabaseManager()
    id = int(id)
    if not db_manager.add_person(id, first_name, last_name):
        return False, "An error occurred while adding the person to the database!"
    return True, None
