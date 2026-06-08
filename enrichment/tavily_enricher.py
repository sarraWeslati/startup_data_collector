import json

from llm.openrouter_client import call_llm
from utils.json_tools import parse_llm_json


def enrich_from_external_sources(
        entity,
        external_text
):

    prompt = f"""
Tu es un expert de l'écosystème startup.

Objectif :

Compléter les champs manquants
à partir des sources externes.

Ne jamais inventer.

Retourne uniquement un JSON.

Format :

{{
    "founders": [],
    "leadership_team": [],
    "employee_count": null,
    "technologies": [],
    "products_services": [],
    "partners": [],
    "customers": [],
    "accelerators": [],
    "incubators": [],
    "awards": [],
    "funding_stage": null,
    "funding_amount": null,
    "investors": [],
    "portfolio_companies": [],
    "hiring": null,
    "open_positions": [],
    "linkedin": null,
    "website": null
}}

Entité :

{json.dumps(entity, ensure_ascii=False)}

Sources :

{external_text[:8000]}
"""

    response = call_llm(
        prompt,
        max_tokens=3000
    )

    return parse_llm_json(response)