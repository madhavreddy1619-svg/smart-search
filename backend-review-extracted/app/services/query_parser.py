import re

TYPO_CORRECTIONS = {
    "suppiles": "supplies",
    "ppl": "people",
    "claasroom": "classroom",
    "monitr": "monitor",
}

FILLER_PHRASES = [
    "i need",
    "help me",
    "please",
    "can you",
]

def clean_query(query: str) -> str:
    cleaned = query.lower().strip()

    for wrong, right in TYPO_CORRECTIONS.items():
        cleaned = re.sub(rf"\b{wrong}\b", right, cleaned)

    for phrase in FILLER_PHRASES:
        cleaned = re.sub(rf"\b{phrase}\b", "", cleaned).strip()

    cleaned = re.sub(r"\s+", " ", cleaned)

    return cleaned

def extract_group_size(query: str):
    match = re.search(r"\b(\d+)\b", query)

    if match:
        return int(match.group(1))

    return None

def parse_query(query: str):
    cleaned_query = clean_query(query)
    group_size = extract_group_size(cleaned_query)

    return {
        "original_query": query,
        "cleaned_query": cleaned_query,
        "group_size": group_size
    }