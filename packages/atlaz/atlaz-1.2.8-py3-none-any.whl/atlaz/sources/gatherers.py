from typing import Optional
from atlaz.sources.utility import normalize_string, check_in_text
from atlaz.sources.fuzz import fuzzy_sequence_match_levenshtein

def gather_exact_match_text(text: str, source_str: str) -> str:
    normalized_source = normalize_string(source_str)
    normalized_text_chars = []
    index_map = []
    for i, ch in enumerate(text):
        if ch not in {' ', '\n', '-'}:
            normalized_text_chars.append(ch.lower())
            index_map.append(i)
    normalized_text = "".join(normalized_text_chars)
    pos = normalized_text.find(normalized_source)
    if pos == -1:
        raise ValueError("No exact match found")
    original_start = index_map[pos]
    original_end = index_map[pos + len(normalized_source) - 1]
    extracted = text[original_start: original_end + 1]
    if normalize_string(extracted) != normalized_source:
        raise ValueError("Normalized extracted substring does not match the normalized token.")
    return extracted

def gather_fuzzy_match(query: str, text: str) -> Optional[str]:
    normalized_query = normalize_string(query)
    normalized_text = normalize_string(text)
    if normalized_query in normalized_text:
        return gather_exact_match_text(text, query)
    matches = fuzzy_sequence_match_levenshtein(query, text, threshold=80, exception_tolerance=0)
    if matches:
        return matches[0]['matched_sequence']
    return None

def extract_start_end_from_text(source_start: str, source_end: str, text: str) -> tuple:
    if check_in_text(text, source_start):
        source_start = gather_exact_match_text(text, source_start)
    else:
        source_start = gather_fuzzy_match(source_start, text)
    if check_in_text(text, source_end):
        source_end = gather_exact_match_text(text, source_end)
    else:
        source_end = gather_fuzzy_match(source_end, text)
    return source_start, source_end