from urllib.parse import urlparse


SOCIAL_DOMAINS = {
    "linkedin": ["linkedin.com/company", "linkedin.com/school", "linkedin.com/in"],
    "facebook": ["facebook.com"],
    "twitter": ["twitter.com", "x.com"],
    "instagram": ["instagram.com"],
    "youtube": ["youtube.com", "youtu.be"],
    "github": ["github.com"],
    "tiktok": ["tiktok.com"],
}


def detect_social_platform(url):
    lower_url = url.lower()

    for platform, patterns in SOCIAL_DOMAINS.items():
        if any(pattern in lower_url for pattern in patterns):
            return platform

    return None


def is_valid_social_url(url):
    if not url:
        return False

    if not url.startswith(("http://", "https://")):
        return False

    parsed = urlparse(url)

    if not parsed.netloc:
        return False

    return detect_social_platform(url) is not None


def extract_social_links_from_text(text):
    social_links = {}

    if not text:
        return social_links

    parts = text.replace(")", " ) ").replace("(", " ( ").split()

    for part in parts:
        if not part.startswith(("http://", "https://")):
            continue

        url = part.strip().strip("[](){}<>\"'.,;")

        if not is_valid_social_url(url):
            continue

        platform = detect_social_platform(url)

        if platform and platform not in social_links:
            social_links[platform] = url

    return social_links


def add_social_links_to_entity(entity, social_links):
    if not isinstance(entity, dict):
        return entity

    if not social_links:
        return entity

    existing_social_links = entity.get("social_links", {})

    if not isinstance(existing_social_links, dict):
        existing_social_links = {}

    for platform, url in social_links.items():
        if platform not in existing_social_links:
            existing_social_links[platform] = url

        if platform == "linkedin" and not entity.get("linkedin"):
            entity["linkedin"] = url

    entity["social_links"] = existing_social_links

    return entity