import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from extractor.entity_extractor import extract_from_url
from collector.site_collector import collect_from_site
from storage.file_storage import save_json, make_filename


def normalize_url(url):
    url = url.strip()

    if not url:
        return None

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return url


def main():
    url = normalize_url(input("Entrer une URL : "))

    if not url:
        print("URL invalide")
        return

    mode = input("Mode (1 = une page, 2 = site complet) : ").strip()

    if mode == "2":
        data = collect_from_site(
            start_url=url,
            max_pages=10,
            max_depth=1,
        )
        filename = "site_collection.json"
    else:
        data = extract_from_url(url)
        filename = make_filename(data)

    if data is None:
        print("Impossible d'extraire les donnees")
        return

    print("\nResultat :")
    print(data)

    save_json(data, filename)


if __name__ == "__main__":
    main()