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


def chunk_text(text, max_chars=6000):
    if not text:
        return []

    return [
        text[index:index + max_chars]
        for index in range(0, len(text), max_chars)
    ]


def split_markdown_blocks(text):
    blocks = []
    current_block = []

    for line in text.splitlines():
        line = line.strip()

        if line.startswith("* ![") and current_block:
            blocks.append("\n".join(current_block))
            current_block = []

        if line:
            current_block.append(line)

    if current_block:
        blocks.append("\n".join(current_block))

    return blocks


def group_blocks(blocks, max_chars=6000):
    groups = []
    current_group = []
    current_size = 0

    for block in blocks:
        block_size = len(block)

        if current_size + block_size > max_chars and current_group:
            groups.append("\n\n".join(current_group))
            current_group = []
            current_size = 0

        current_group.append(block)
        current_size += block_size

    if current_group:
        groups.append("\n\n".join(current_group))

    return groups


def smart_chunker(text, max_chars=6000):
    if not text:
        return []

    blocks = split_markdown_blocks(text)

    # Si on trouve plusieurs blocs structurés, on les groupe sans couper les entités.
    if len(blocks) > 3:
        return group_blocks(blocks, max_chars=max_chars)

    # Sinon, fallback classique.
    return chunk_text(text, max_chars=max_chars)
