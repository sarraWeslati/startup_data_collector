from html.parser import HTMLParser
from urllib.request import Request, urlopen


class SimpleTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip_tag = None

    def handle_starttag(self, tag, attrs):
        if tag in ["script", "style", "noscript"]:
            self.skip_tag = tag

        if tag in ["p", "div", "section", "article", "br", "li", "h1", "h2", "h3"]:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag == self.skip_tag:
            self.skip_tag = None

        if tag in ["p", "div", "section", "article", "li", "h1", "h2", "h3"]:
            self.parts.append("\n")

    def handle_data(self, data):
        if self.skip_tag:
            return

        data = data.strip()

        if data:
            self.parts.append(data)

    def get_text(self):
        return " ".join(self.parts)


def fallback_fetch_url(url):
    """
    Crawler de secours sans crawl4ai.
    Il utilise seulement Python standard.
    """
    request = Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/137.0.0.0 Safari/537.36"
            )
        },
    )

    with urlopen(request, timeout=30) as response:
        html = response.read().decode("utf-8", errors="ignore")

    parser = SimpleTextExtractor()
    parser.feed(html)

    return parser.get_text()


async def crawl_url(url):
    """
    Essaie d'abord crawl4ai.
    Si crawl4ai bloque ou echoue, utilise un crawler simple de secours.
    """
    try:
        from crawl4ai import AsyncWebCrawler

        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url)
            return result.markdown

    except Exception as error:
        print(f"Erreur crawl4ai : {error}")
        print("Tentative avec le crawler fallback...")

        try:
            return fallback_fetch_url(url)
        except Exception as fallback_error:
            print(f"Erreur fallback crawler : {fallback_error}")
            return None