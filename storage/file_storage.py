import json
import re
from pathlib import Path


def save_json(data, filename):
    output_dir = Path("extracted_json")
    output_dir.mkdir(exist_ok=True)

    file_path = output_dir / filename

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print(f"Fichier JSON sauvegarde : {file_path}")


def save_markdown(content, filename):
    output_dir = Path("raw_data")
    output_dir.mkdir(exist_ok=True)

    file_path = output_dir / filename

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    print(f"Markdown sauvegarde : {file_path}")


def make_filename(data):
    if isinstance(data, list):
        return "multiple_entities.json"

    name = (
        data.get("startup_name")
        or data.get("investor_name")
        or data.get("name")
        or "entity"
    )

    filename = name.lower().strip()
    filename = re.sub(r"[^a-z0-9_-]+", "_", filename)
    filename = filename.strip("_")

    if not filename:
        filename = "entity"

    return f"{filename}.json"
