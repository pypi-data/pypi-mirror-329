from atlaz.sources.utility import check_in_text, get_name_from_entity
from atlaz.sources.interface import gather_source_scores_entities
from atlaz.sources.gatherers import gather_exact_match_text
from atlaz.sources.validators import validate_source_token_limit

def validate_sources(generated_graph_extension: dict, text: str):
    """
    Validate the sources in the generated graph extension.
    """
    list_of_obj = []
    for key, value in generated_graph_extension.items():
        list_of_obj.append(({"Name": key, "TextSource": value["TextSource"]}, get_name_from_entity))
    errors_entities, complexity_entities = gather_source_scores_entities(list_of_obj, text)
    return errors_entities

def build_full_source(source_start: str, source_end: str, text: str) -> str:
    if check_in_text(text, source_start):
        source_start = gather_exact_match_text(text, source_start)
    if check_in_text(text, source_end):
        source_end = gather_exact_match_text(text, source_end)
    return validate_source_token_limit(source_start, source_end, "entity_name", text=text, max_tokens=750, extract_source=True)