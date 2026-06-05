from urllib import response

from llm.openrouter_client import call_llm
from utils.json_tools import parse_llm_json


def extract_general_entity_info(text, source_url):
    prompt = f"""
Tu es un systeme d'extraction de donnees sur l'ecosysteme startup.

Retourne uniquement un JSON valide.
N'utilise pas Markdown.
N'invente jamais une information.
Si une information est absente, mets null ou [].

Regle tres importante :
Ne classe une entite comme "startup" que si c'est clairement une entreprise startup qui vend un produit ou service.
Si l'entite accompagne, finance, incube, accelere ou forme des startups, ce n'est pas une startup.

Types autorises :
- startup
- investor
- venture_capital_fund
- incubator
- accelerator
- support_organization
- startup_directory
- investor_directory
- unknown

Si la page contient plusieurs entites, retourne un tableau JSON.

Pour une startup :
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

Pour un investisseur, incubateur, accelerateur ou organisation de support :
{{
  "entity_type": null,
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

    response = call_llm(prompt, max_tokens=8000)
    return parse_llm_json(response)