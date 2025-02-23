import re

BIAS_PATTERNS = [
    (r"\b(best|perfect|flawless|#1|unbeatable)\b", "excellence claims"),
    (r"\b(guarantee|promise|assure)\b", "absolute commitments"),
    (r"\b(never|always|forever)\b", "absolute terms")
]

def detect_and_correct_bias(response):
    corrections = []
    for pattern, label in BIAS_PATTERNS:
        if re.search(pattern, response, flags=re.I):
            corrections.append(label)
    
    if corrections:
        return f"Based on verified information: {re.sub(r'!\?$', '.', response.strip())}"
    return response
