import asyncio

from crawler.crawl4ai_extractor import crawl_url
from utils.text_processing import clean_text


def collect_social_text(entity):
    texts = []

    social_links = entity.get("social_links", {})

    for platform, url in social_links.items():

        print(f"Collecte source sociale : {platform}")

        try:
            markdown = asyncio.run(crawl_url(url))

            if markdown:
                cleaned = clean_text(markdown)

                if cleaned:
                    texts.append(
                        f"\nSOURCE={platform}\n{cleaned}"
                    )

        except Exception as error:
            print(error)

    return "\n\n".join(texts)