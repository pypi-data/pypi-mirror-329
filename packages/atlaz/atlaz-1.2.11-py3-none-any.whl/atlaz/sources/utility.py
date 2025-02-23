import re

def handle_error_messages(error_messages: list, initial_complexity_level: int, new_error_message: str, complexity_level: int) -> tuple:
    """Overwrite the error messages if the complexity level is lower, or append if the same"""
    if initial_complexity_level == complexity_level:
        error_messages.append(new_error_message)
    elif new_error_message == '':
        return error_messages, initial_complexity_level
    elif initial_complexity_level > complexity_level:
        error_messages = [new_error_message]
        initial_complexity_level = complexity_level
    return error_messages, initial_complexity_level

def clean_source(source: str) -> str:
    """Cleans the source"""
    if source[-3:] ==  '...':
        source = source[:-3]
    if source[:3] == '...':
        source = source[3:]
    return source

def merge_with_overlap(source_start: str, source_end: str) -> str:
    """
    Merges two strings if there is an overlap between the end of the first string
    and the start of the second string.
    """
    max_overlap = 0
    for i in range(1, len(source_start) + 1):
        if source_start[-i:] == source_end[:i]:
            max_overlap = i
    merged_string = source_start + source_end[max_overlap:]
    return merged_string

def normalize_string(s: str) -> str:
    s = s.lower()
    s = re.sub(r'-\s*\n\s*', '', s)
    return re.sub(r'[ \n\-]', '', s)

def normalize_for_fuzzy(s: str) -> str:
    return re.sub(r'[^\w\s]', '', s).lower()

def check_in_text(text: str, source_str: str) -> bool:
    verdict =  normalize_string(source_str) in normalize_string(text)
    return verdict

def get_name_from_entity(entity: dict) -> str:
    """Gets the name from the entity"""
    return entity["Name"]

def get_name_from_relationship_entity(entity: dict) -> str:
    """Gets the name from the relationship entity"""
    return f'the relationship with ID: ' + str(entity["ID"])