from llm.openrouter_client import call_llm
from utils.json_tools import parse_llm_json


def extract_startup_info(text, source_url):
    """
    Extrait les champs startup definis dans le document Word.
    """
    prompt = f"""
Tu es un systeme d'extraction de donnees sur les startups.

Retourne uniquement un JSON valide.
N'utilise pas Markdown.
N'invente jamais une information.
Si une information est absente, mets null ou [].

Format attendu :
{{
  "entity_type": "startup",
  "startup_name": null,
  "sector": null,
  "description": null,
  "country": null,
  "city": null,
  "founding_year": null,
  "founders": [],
  "website": null,
  "email": null,
  "linkedin": null,
  "status": null,
  "startup_stage": null,
  "investors": [],
  "source_url": "{source_url}"
}}

Texte :
{text}
"""

    response = call_llm(prompt)
    return parse_llm_json(response)
