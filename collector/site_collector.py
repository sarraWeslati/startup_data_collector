import asyncio
from collections import deque

from crawler.crawl4ai_extractor import crawl_url
from extractor.entity_extractor import extract_from_markdown
from utils.link_extractor import extract_links_from_markdown


def flatten_results(results):
    final = []

    for item in results:
        if isinstance(item, list):
            final.extend(item)
        elif isinstance(item, dict):
            final.append(item)

    return final


def collect_from_site(start_url, max_pages=10, max_depth=1):
    visited = set()
    queue = deque()
    all_results = []

    queue.append((start_url, 0))

    while queue and len(visited) < max_pages:
        current_url, depth = queue.popleft()

        if current_url in visited:
            continue

        print(f"\nCollecte page {len(visited) + 1}/{max_pages} : {current_url}")

        visited.add(current_url)

        markdown = asyncio.run(crawl_url(current_url))

        if not markdown:
            continue

        data = extract_from_markdown(markdown, current_url)

        if data:
            all_results.append(data)

        if depth >= max_depth:
            continue

        links = extract_links_from_markdown(markdown, current_url)

        for link in links:
            if link not in visited:
                queue.append((link, depth + 1))

    return deduplicate_entities(flatten_results(all_results))

def get_entity_name(item):
    return (
        item.get("startup_name")
        or item.get("investor_name")
        or item.get("name")
        or ""
    )


def deduplicate_entities(items):
    unique = []
    seen = set()

    for item in items:
        if not isinstance(item, dict):
            continue

        name = get_entity_name(item).lower().strip()
        entity_type = item.get("entity_type", "unknown")

        key = f"{entity_type}:{name}"

        if not name:
            unique.append(item)
            continue

        if key in seen:
            continue

        seen.add(key)
        unique.append(item)

    return unique