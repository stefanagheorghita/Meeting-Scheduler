from database.manager import DatabaseManager


def format_name(name):
    """
    It formats the name to have the first letter of each word capitalized.
    :param name:
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
    :param name:
    :param sep:
    :return: True if the name is valid, False otherwise.
    """
    parts = name.split(sep)
    for part in parts:
        if all(char.isspace() for char in part):
            return False
    return True


def validate_name(name):
    """
    Validates the basic rules for a name. The name must contain only letters, spaces, dashes or apostrophes.
    :param name:
    :return: (True, None) if the name is valid, (False, error message) otherwise.
    """
    name = name.strip()
    n_chr = [c for c in name if c.isalpha() or c == " " or c == "-" or c == "'"]
    name = name.strip()
    if name.startswith("-") or name.endswith("-") or name.startswith("'") or name.endswith("'"):
        return False, "Invalid format for first name!"
    if len(n_chr) != len(name):
        return False, "First name must contain only letters!"
    if not validate_consecutive(name, "-"):
        return False, "Invalid format for first name!"
    if not validate_consecutive(name, "'"):
        return False, "Invalid format for first name!"
    return True, None


def add_person_validation(id, first_name, last_name):
    """
    Validates the fields of the add person window and adds the person to the database
    :param id:
    :param first_name:
    :param last_name:
    :return: (True, message) if the fields are valid, (False, error message) otherwise.
    """
    message = None
    if id == "" or first_name == "" or last_name == "":
        return False, "All fields must be filled!"
    if not id.isdigit():
        return False, "Id must be a number!"
    if int(id) <= 0 or int(id) > 2147483647:
        return False, "The id is not within the limits!"
    result, msg = validate_name(first_name)
    if not result:
        return False, msg
    db_manager = DatabaseManager()
    id = int(id)
    if not db_manager.search_id_db(id):
        return False, "There is already a person in the database with the given id!"
    first_name_formatted = format_name(first_name)
    last_name_formatted = format_name(last_name)
    if first_name_formatted != first_name or last_name_formatted != last_name:
        message = "The person was added to the database with the following name: "
        message += first_name_formatted + " " + last_name_formatted
    if not db_manager.add_person(id, first_name, last_name):
        return False, "An error occurred while adding the person to the database!"
    return True, message
