from urllib.parse import urljoin, urlparse, urldefrag


IGNORED_EXTENSIONS = (
    ".svg", ".png", ".jpg", ".jpeg", ".gif", ".webp",
    ".pdf", ".zip", ".rar", ".css", ".js", ".ico",
)


IGNORED_PATTERNS = (
    "storage/",
    "uploads/",
    "images/",
    "assets/",
    "facebook.com",
    "linkedin.com",
    "twitter.com",
    "instagram.com",
    "youtube.com",
)


def normalize_link(base_url, link):
    if not link:
        return None

    absolute_url = urljoin(base_url, link)
    absolute_url, _ = urldefrag(absolute_url)

    return absolute_url


def is_same_domain(url, base_domain):
    try:
        return urlparse(url).netloc == base_domain
    except Exception:
        return False


def should_ignore_link(url):
    lower_url = url.lower()

    if lower_url.endswith(IGNORED_EXTENSIONS):
        return True

    if any(pattern in lower_url for pattern in IGNORED_PATTERNS):
        return True

    return False


def extract_links_from_markdown(markdown, base_url):
    links = []
    base_domain = urlparse(base_url).netloc

    for part in markdown.split("("):
        if ")" not in part:
            continue

        link = part.split(")", 1)[0].strip()
        link = normalize_link(base_url, link)

        if not link:
            continue

        if not link.startswith(("http://", "https://")):
            continue

        if not is_same_domain(link, base_domain):
            continue

        if should_ignore_link(link):
            continue

        if link not in links:
            links.append(link)

    return links