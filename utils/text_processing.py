def clean_text(text):
    """
    Nettoie le texte brut avant l'envoi au LLM.
    """
    if not text:
        return ""

    unwanted_words = [
        "cookie",
        "cookies",
        "privacy policy",
        "terms of service",
        "all rights reserved",
        "subscribe",
        "newsletter",
        "accept all",
        "manage preferences",
    ]

    cleaned_lines = []

    for line in text.splitlines():
        line = line.strip()

        if len(line) < 3:
            continue

        lower_line = line.lower()

        if any(word in lower_line for word in unwanted_words):
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def chunk_text(text, max_chars=3000):
    """
    Decoupe un long texte en blocs pour eviter de depasser le contexte du LLM.
    """
    if not text:
        return []

    return [
        text[index:index + max_chars]
        for index in range(0, len(text), max_chars)
    ]
