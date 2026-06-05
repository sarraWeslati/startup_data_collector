import asyncio

from crawler.crawl4ai_extractor import crawl_url
from extractor.entity_detector import detect_entity_type
from extractor.general_extractor import extract_general_entity_info
from extractor.investor_extractor import extract_investor_info
from extractor.startup_extractor import extract_startup_info
from storage.file_storage import save_markdown
from utils.json_tools import merge_entities
from utils.text_processing import clean_text, smart_chunker 
from utils.normalization import normalize_data


def extract_from_url(url):
    markdown = asyncio.run(crawl_url(url))

    if not markdown:
        return None

    return extract_from_markdown(markdown, url)

def extract_from_markdown(markdown, url):
    if not markdown:
        return None

    save_markdown(markdown, "last_page.md")

    cleaned_text = clean_text(markdown)

    if not cleaned_text:
        return None

    detected = detect_entity_type(cleaned_text)
    entity_type = detected.get("entity_type", "unknown")

    chunks = smart_chunker(cleaned_text, max_chars=6000)
    extracted_results = []

    for chunk in chunks:
        if entity_type == "startup":
            result = extract_startup_info(chunk, url)
        elif entity_type in ["investor", "venture_capital_fund"]:
            result = extract_investor_info(chunk, url)
        else:
            result = extract_general_entity_info(chunk, url)

        if result:
            extracted_results.append(result)

    final_data = merge_entities(extracted_results)

    if isinstance(final_data, dict):
        final_data["source_url"] = url
        final_data["detected_entity_type"] = entity_type

    if isinstance(final_data, list):
        for item in final_data:
            if isinstance(item, dict):
                item["source_url"] = url

    final_data = normalize_data(final_data)

    return final_data