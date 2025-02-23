from atlaz.sources.utility import merge_with_overlap, check_in_text
from atlaz.sources.fuzz import extract_sources, check_fuzzy_match
from atlaz.sources.gatherers import extract_start_end_from_text, gather_fuzzy_match
from atlaz.sources.gatherers import gather_exact_match_text
from atlaz.utility import count_tokens

def validate_source_exists(source_start: str, source_end: str, entity_name: str, text: str) -> str:
    """Basic case that a match exists at all"""
    if source_start is None or source_end is None:
        raise ValueError(f'{source_start=}, {source_end=}')
    if not check_in_text(text, source_start) and not(check_fuzzy_match(source_start, text)):
        error = f"'StartOfSource': '{source_start}' not found in the text for '{entity_name}'."
        return error
    elif not check_in_text(text, source_end) and not(check_fuzzy_match(source_end, text)):
        error = f"'EndOfSource': '{source_end}' not found in the text for '{entity_name}'."
        return error
    elif source_start == '' or source_end == '':
        error = f"'StartOfSource' and 'EndOfSource' cannot be empty for '{entity_name}'."
        return error
    return ''

def validate_source_unique(source_start: str, source_end: str, entity_name: str, text: str, rec = False) -> str:
    """More advanced case that a match exists exactly once"""
    if source_start == source_end:
        occurrences = text.count(source_start)
        if occurrences == 1:
            return ''
        else:
            return (
                f"Found {occurrences} occurrences of '{source_start}', "
                "we expected exactly one, and StartOfSource and EndOfSource are not supposed to be identical, they are supposed to be a searchable match of the start and end of the source."
            )
    valid_refs = check_in_text(text, source_start) and check_in_text(text, source_end)
    if valid_refs:
        valid_pairs = extract_sources(source_start, source_end, text)
        if len(valid_pairs) != 1:
            concat = f"{source_start} {source_end}"
            combined_match_count = text.count(concat)
            if combined_match_count != 1:
                start_idx = text.find(source_start)
                end_idx = text.find(source_end)
                if start_idx != -1 and end_idx != -1 and end_idx < start_idx:
                    return (
                        f"'EndOfSource' (`{source_end}`) appears in the text before "
                        f"'StartOfSource' (`{source_start}`) for '{entity_name}'. "
                        "Please reverse or correct these so the start precedes the end in the actual text, unless this wasn't a correct source to begin with"
                    )
                merged_reference = merge_with_overlap(source_start, source_end)
                combined_match_count = text.count(merged_reference)
                if combined_match_count != 1:
                    if source_start == source_end:
                        return f"{source_start} was used both as StartOfSource and EndOfSource for '{entity_name}'. This is not allowed, the start should be a searchable match of the start of the source and the end should be a searchable match of the end of the source."
                    error = (
                        f"There was not exactly one occurrence where '{source_start}' "
                        f"appears before '{source_end}'. This creates ambiguity for '{entity_name}'. "
                        "Adjust the source so it's uniquely identifiable."
                    )
                    return error
                else:
                    return ''
            else:
                return ''
        else:
            return ''
    else:
        return validate_fuzzy_source_unique(source_start, source_end, entity_name, text, rec = True)

def validate_fuzzy_source_unique(source_start: str, source_end: str, entity_name: str, text: str, rec = False) -> str:
    if not rec:
        if not check_in_text(text, source_start):
            fuzzy_source_start = gather_fuzzy_match(source_start, text)
            if not fuzzy_source_start:
                error = f"'StartOfSource': '{source_start}' not found in the text for '{entity_name}'."
                fuzzy_source_start = source_start
                return error
        else:
            fuzzy_source_start = source_start
        if not check_in_text(text, source_end):
            fuzzy_source_end = gather_fuzzy_match(source_end, text)
            if not fuzzy_source_end:
                error = f"'EndOfSource': '{source_end}' not found in the text for '{entity_name}'."
                fuzzy_source_end = source_end
                return error
        else:
            fuzzy_source_end = source_end
        if not fuzzy_source_start or not fuzzy_source_end:
            raise ValueError(f'{fuzzy_source_start=}, {fuzzy_source_end=}')
        return validate_source_unique(fuzzy_source_start, fuzzy_source_end, entity_name, text, rec = True)
    return ''

def merge_start_end(source_start: str, source_end: str, text: str) -> str:
    valid_pairs = extract_sources(source_start, source_end, text)
    if len(valid_pairs) != 1:
        enclosed_text = f"{source_start} {source_end}"
    else:
        start, end = valid_pairs[0]
        enclosed_text = text[start:end + len(source_end)]
    return enclosed_text

def validate_source_token_limit(source_start: str, source_end: str, entity_name: str, text: str, max_tokens: int, extract_source = False) -> str:
    """Validates the source reference against the token limit."""
    if source_start is None or source_end is None:
        raise ValueError(f'validate_source_token_limit {source_start=}, {source_end=}')
    #print(f'{source_start=}, {source_end=}')
    """
    if not source_start or not source_end:
        raise ValueError(f'{source_start=}, {source_end=}')
    if not check_in_text(text, source_start) or not check_in_text(text, source_end):
        raise ValueError(f'{source_start=}, {source_end=}')"""
    enclosed_text = merge_start_end(source_start, source_end, text) 
    token_count = count_tokens(enclosed_text)
    if token_count > max_tokens:
        error = (
            f"The source reference for '{entity_name}' is too long, it shouldn't be more than a paragraph."
        )
        return error
    return '' 


def validate_layers(source_start: str, source_end: str, entity_name: str, text: str) -> list:
    """Validates the source against the text and produces feedback"""
    level_0 = validate_source_exists(source_start, source_end, entity_name, text)
    if level_0 != '':
        return level_0, 0, None
    source_start, source_end = extract_start_end_from_text(source_start, source_end, text)
    level_1 = validate_source_unique(source_start, source_end, entity_name, text)
    if level_1 != '':
        return level_1, 1, None
    level_2 = validate_source_token_limit(source_start, source_end, entity_name, text, 750)
    if level_2 != '':
        return level_2, 2, None
    final_source =  merge_start_end(source_start, source_end, text=text)
    return '', 3, final_source

def validate_source_against_text(source_start: str, source_end: str, entity_name: str, text: str) -> list:
    """Validates the source against the text and produces feedback"""
    hack = ['Ingen information']
    if source_start in hack:
        _level = f'<{source_start}> är inte en källhänvisning, det är otroligt respektlöst att inkludera källan om det inte finns någon information att hänvisa till.'
        return _level, -1 
    elif source_end in hack:
        _level = f'<{source_end}> är inte en källhänvisning, det är otroligt respektlöst att inkludera källan om det inte finns någon information att hänvisa till.'
        return _level, -1 
    level_0 = validate_source_exists(source_start, source_end, entity_name, text)
    if level_0 != '':
        return level_0, 0
    if check_in_text(text, source_start):
        source_start = gather_exact_match_text(text, source_start)
    if check_in_text(text, source_end):
        source_end = gather_exact_match_text(text, source_end)
    level_1 = validate_source_unique(source_start, source_end, entity_name, text)
    if level_1 != '':
        return level_1, 1
    level_2 = validate_source_token_limit(source_start, source_end, entity_name, text, 750)
    if level_2 != '':
        return level_2, 2
    return '', 3