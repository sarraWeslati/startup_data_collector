from llm.openrouter_client import call_llm
from utils.json_tools import parse_llm_json


def detect_entity_type(text):
    """
    Detecte si la page parle d'une startup, d'un investisseur, d'un annuaire, etc.
    """
    prompt = f"""
Tu es un systeme de classification de pages web liees aux startups.

Retourne uniquement un JSON valide.
N'utilise pas Markdown.

Types possibles :
- startup
- investor
- venture_capital_fund
- incubator
- accelerator
- startup_directory
- investor_directory
- unknown

Format attendu :
{{
  "entity_type": "",
  "reason": ""
}}

Texte :
{text[:5000]}
"""

    response = call_llm(prompt, max_tokens=500)
    return parse_llm_json(response)
