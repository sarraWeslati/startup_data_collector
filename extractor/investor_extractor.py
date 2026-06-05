from llm.openrouter_client import call_llm
from utils.json_tools import parse_llm_json


def extract_investor_info(text, source_url):
    """
    Extrait les champs investisseur definis dans le document Word.
    """
    prompt = f"""
Tu es un systeme d'extraction de donnees sur les investisseurs.

Retourne uniquement un JSON valide.
N'utilise pas Markdown.
N'invente jamais une information.
Si une information est absente, mets null ou [].

Format attendu :
{{
  "entity_type": "investor",
  "investor_name": null,
  "investor_type": null,
  "website": null,
  "country": null,
  "description": null,
  "investment_sectors": [],
  "total_investments": null,
  "source_url": "{source_url}"
}}

Texte :
{text}
"""

    response = call_llm(prompt)
    return parse_llm_json(response)
