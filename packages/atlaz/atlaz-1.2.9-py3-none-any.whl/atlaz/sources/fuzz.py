import re
from Levenshtein import distance # type: ignore

def extract_sources(source_start: str, source_end: str, text: str) -> list:
    """Extracts the first valid source pair from the text."""
    start_positions = [i for i in range(len(text)) if text.startswith(source_start, i)]
    end_positions = [i for i in range(len(text)) if text.startswith(source_end, i)]
    valid_pairs = []
    for start in start_positions:
        subsequent_ends = [end for end in end_positions if end > start]
        if subsequent_ends:
            first_end = min(subsequent_ends)
            valid_pairs.append((start, first_end))
    return valid_pairs

def get_word_positions(text: str) -> list:
    """
    Splits the text into words and records the start and end character indices of each word.
    """
    word_positions = []
    for match in re.finditer(r'\b\w+\b', text):
        word = match.group()
        start_idx = match.start()
        end_idx = match.end()
        word_positions.append((word, start_idx, end_idx))
    return word_positions

def fuzzy_sequence_match_levenshtein(query, text, threshold=80, exception_tolerance=1):
    """
    Finds matches of a query string (sequence of words) within a target string using Levenshtein Distance.
    The score is normalized to 0-100 and assigns a perfect score (100) if a query word is a substring of the target word.
    """
    query_words = query.split()
    word_positions = get_word_positions(text)
    target_words = [wp[0] for wp in word_positions]
    matches = []
    for i in range(len(target_words) - len(query_words) + 1):
        subsequence = target_words[i:i + len(query_words)]
        scores = []
        for qw, sw in zip(query_words, subsequence):
            if qw in sw:
                scores.append(100)
            else:
                lev_distance = distance(qw, sw)
                max_length = max(len(qw), len(sw))
                normalized_score = 100 * (1 - lev_distance / max_length) if max_length > 0 else 100
                scores.append(normalized_score)
        exceptions = sum(1 for score in scores if score < threshold)
        if exceptions <= exception_tolerance:
            avg_score = sum(scores) / len(scores)
            if avg_score >= threshold:
                start_char = word_positions[i][1]
                end_char = word_positions[i + len(query_words) - 1][2]
                exact_substring = text[start_char:end_char]
                matches.append({
                    "matched_sequence": exact_substring,
                    "average_score": avg_score,
                    "exceptions": exceptions,
                    "start_char": start_char,
                    "end_char": end_char
                })
    matches.sort(key=lambda x: x['average_score'], reverse=True)
    perfect_matches = [match for match in matches if match['average_score'] == 100]
    if perfect_matches:
        return perfect_matches
    if matches:
        best_score = matches[0]['average_score']
        top_matches = [match for match in matches if match['average_score'] >= best_score - 5]
        return top_matches[:5]
    return []
def check_fuzzy_match(query: str, text: str) -> bool:
    matches = fuzzy_sequence_match_levenshtein(query, text, threshold=80, exception_tolerance=0)
    return len(matches) > 0

