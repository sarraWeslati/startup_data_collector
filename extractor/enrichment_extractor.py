import asyncio
import json

from crawler.crawl4ai_extractor import crawl_url
from llm.openrouter_client import call_llm
from utils import social_links
from utils.json_tools import parse_llm_json
from utils.text_processing import clean_text, smart_chunker
from utils.social_links import extract_social_links_from_text, add_social_links_to_entity
from extractor.social_enrichment_extractor import collect_social_text
from utils.confidence_score import compute_confidence_score

def get_enrichment_urls(entity, use_linkedin=False):
    urls = []

    website = entity.get("website")
    linkedin = entity.get("linkedin")

    if website:
        urls.append(website)

    if use_linkedin and linkedin:
        urls.append(linkedin)

    return urls


def merge_entity_data(original, enriched):

    if not isinstance(enriched, dict):
        return original

    for key, value in enriched.items():

        # ignorer les valeurs vides
        if value in [None, "", []]:
            continue

        current_value = original.get(key)

        # champ vide dans l'entité originale
        if current_value in [None, "", []]:
            original[key] = value
            continue

        # fusion des listes
        if (
            isinstance(current_value, list)
            and isinstance(value, list)
        ):

            merged = []

            for item in current_value + value:

                if item not in merged:
                    merged.append(item)

            original[key] = merged
            continue

        # fusion des dictionnaires
        if (
            isinstance(current_value, dict)
            and isinstance(value, dict)
        ):

            merged = current_value.copy()

            for sub_key, sub_value in value.items():

                if sub_value not in [None, "", [], {}]:
                    merged[sub_key] = sub_value

            original[key] = merged
            continue

        # garder la description la plus riche
        if (
            key == "description"
            and isinstance(value, str)
        ):

            if len(value) > len(str(current_value)):
                original[key] = value

            continue

        # remplacer les chaînes plus informatives
        if (
            isinstance(current_value, str)
            and isinstance(value, str)
        ):

            if len(value) > len(current_value):
                original[key] = value

            continue

    return original


def extract_complementary_info(entity, page_text, source_url):
    prompt = f"""
Tu es un systeme d'enrichissement de donnees startup/investisseur.

Objectif :
Completer les champs manquants de l'entite existante avec les informations trouvees dans la page.

Regles :
- Retourne uniquement un JSON valide.
- N'utilise pas Markdown.
- N'invente jamais une information.
- Si une information est absente, garde null ou [].
- Ne change pas le nom de l'entite sauf correction evidente.
- Complete surtout : email, linkedin, founders, city, country, founding_year, sector, description, status, startup_stage, investors.

Entite existante :
{json.dumps(entity, ensure_ascii=False, indent=2)}

Source consultee :
{source_url}

Texte de la page :
{page_text[:7000]}
"""

    response = call_llm(prompt, max_tokens=3000)
    return parse_llm_json(response)


def enrich_entity(entity, use_linkedin=False):

    urls = get_enrichment_urls(
        entity,
        use_linkedin=use_linkedin
    )

    if not urls:
        return entity

    enrichment_sources = entity.get(
        "enrichment_sources",
        []
    )

    failed_sources = entity.get(
        "failed_enrichment_sources",
        []
    )

    # ==========================
    # ENRICHISSEMENT SITE WEB
    # ==========================

    for url in urls:

        print(f"Enrichissement : {url}")

        markdown = asyncio.run(
            crawl_url(url)
        )

        if not markdown:

            if url not in failed_sources:
                failed_sources.append(url)

            continue

        cleaned_text = clean_text(markdown)

        if not cleaned_text:

            if url not in failed_sources:
                failed_sources.append(url)

            continue

        social_links = extract_social_links_from_text(
            markdown
        )

        entity = add_social_links_to_entity(
            entity,
            social_links
        )

        chunks = smart_chunker(
            cleaned_text,
            max_chars=6000
        )

        for chunk in chunks[:2]:

            enriched = extract_complementary_info(
                entity,
                chunk,
                url
            )

            entity = merge_entity_data(
                entity,
                enriched
            )

        if url not in enrichment_sources:
            enrichment_sources.append(url)

    # ==========================
    # ENRICHISSEMENT SOCIAL
    # ==========================

    social_text = collect_social_text(entity)

    if social_text:

        advanced_data = extract_advanced_info(
            entity,
            social_text[:7000]
        )

        entity = merge_entity_data(
            entity,
            advanced_data
        )

    # ==========================
    # ENRICHISSEMENT TAVILY
    # ==========================

    try:

        from enrichment.tavily_search import (
            search_entity_sources
        )

        from enrichment.source_collector import (
            collect_source_texts
        )

        from enrichment.tavily_enricher import (
            enrich_from_external_sources
        )

        results = search_entity_sources(
            entity
        )

        if results:

            external_texts = collect_source_texts(
                results
            )

            if external_texts:

                advanced_data = (
                    enrich_from_external_sources(
                        entity,
                        external_texts[:6000]
                    )
                )

                entity = merge_entity_data(
                    entity,
                    advanced_data
                )

    except Exception as error:

        print(
            f"Erreur Tavily : {error}"
        )

    # ==========================
    # METADONNEES
    # ==========================

    entity["enrichment_sources"] = (
        enrichment_sources
    )

    entity["failed_enrichment_sources"] = (
        failed_sources
    )

    entity["social_links_found"] = bool(
        entity.get("social_links")
    )

    entity["confidence_score"] = (
        compute_confidence_score(entity)
    )

    return entity


def enrich_entities(entities, use_linkedin=False, max_entities=10):
    enriched_entities = []

    for index, entity in enumerate(entities):
        if index >= max_entities:
            enriched_entities.append(entity)
            continue

        if isinstance(entity, dict):
            entity = enrich_entity(entity, use_linkedin=use_linkedin)

        enriched_entities.append(entity)

    return enriched_entities

def extract_advanced_info(entity, text):

    prompt = f"""
        Tu es un système expert en enrichissement de startups et investisseurs.

        À partir des informations collectées depuis :

        - site officiel
        - réseaux sociaux publics
        - autres sources publiques

        complète uniquement les informations trouvées.

        Ne jamais inventer.

        Retourne uniquement un JSON valide.

        Format :

        {{
            "legal_name": null,
            "tagline": null,
            "address": null,
            "phone": null,
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
            "hiring": null,
            "open_positions": []
        }}

        Entity :

        {json.dumps(entity, ensure_ascii=False)}

        Text :

        {text[:10000]}
        """

    response = call_llm(prompt, max_tokens=3000)

    return parse_llm_json(response)