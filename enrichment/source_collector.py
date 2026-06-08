import asyncio

from crawler.crawl4ai_extractor import crawl_url
from utils.text_processing import clean_text


def collect_source_texts(results):

    texts = []

    for item in results:

        content = item.get("content")

        if content:

            texts.append(
                clean_text(content)
            )

            continue

        url = item.get("url")

        if not url:
            continue

        print(
            f"Collecte Tavily : {url}"
        )

        try:

            markdown = asyncio.run(
                crawl_url(url)
            )

            if markdown:

                texts.append(
                    clean_text(markdown)
                )

        except Exception as error:

            print(error)

    return "\n\n".join(texts)