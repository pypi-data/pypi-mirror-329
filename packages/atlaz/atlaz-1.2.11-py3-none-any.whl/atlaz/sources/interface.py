from atlaz.sources.utility import clean_source, handle_error_messages
from atlaz.sources.validators import validate_layers
from atlaz.sources.gatherers import extract_start_end_from_text
from atlaz.sources.validators import merge_start_end

def validate_entity_against_text(entity_name: str, entity: dict, text: str, last_level = 0, valid_entities = [], error_messages = [], initial_complexity_level = 10, type_relationship_id = 3) -> list:
    """Validates the entity against the text and produces feedback"""
    if ("SourceNodeID" in entity and "TargetNodeID" in entity and
            entity.get("EntityID") == type_relationship_id):
        return valid_entities, error_messages, initial_complexity_level
    source_start = clean_source(entity["TextSource"]["StartOfSource"])
    source_end = clean_source(entity["TextSource"]["EndOfSource"])
    new_error_message, complexity_level, final_source = validate_layers(source_start, source_end, entity_name, text)
    if complexity_level > last_level:
        valid_entities.append(entity)
    error_messages, initial_complexity_level = handle_error_messages(error_messages, initial_complexity_level, new_error_message, complexity_level)
    return valid_entities, error_messages, initial_complexity_level, final_source

def gather_source_scores_entities(new_entities: list, text: str, last_level = 0, type_relationship_id = 3) -> list:
    """Traverses through entities and gathers source feedback"""
    error_messages = []
    initial_complexity_level = 10
    valid_entities = []
    for entity, get_name_function in new_entities:
        entity_name = get_name_function(entity)
        valid_entities_temp, error_messages, initial_complexity_level, final_source = validate_entity_against_text(
            entity_name, entity, text, last_level, valid_entities, error_messages, initial_complexity_level, type_relationship_id
        )
        valid_entities = [(entity, get_name_function) for entity in valid_entities_temp]
    if len(new_entities) == 0:
        return error_messages, initial_complexity_level
    elif len(error_messages) / len(new_entities) < 0.00:
        return gather_source_scores_entities(valid_entities, text, initial_complexity_level)
    else:
        return error_messages, initial_complexity_level
    
def build_full_source(source_start: str, source_end: str, text: str) -> str:
    source_start, source_end = extract_start_end_from_text(source_start, source_end, text)
    if source_start is None or source_end is None:
        raise ValueError(f'BUILD_FULL_SOURCE: {source_start=}, {source_end=}')
    return merge_start_end(source_start, source_end, text=text)