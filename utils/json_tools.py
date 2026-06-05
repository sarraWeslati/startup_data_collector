import json


def parse_llm_json(response):
    """
    Convertit la reponse du LLM en JSON Python.
    """
    if not response:
        return None

    response = response.strip()
    response = response.replace("```json", "")
    response = response.replace("```", "")
    response = response.strip()

    return json.loads(response)


def merge_entities(results):
    """
    Fusionne plusieurs resultats JSON partiels en un seul resultat final.
    """
    if not results:
        return None

    if all(isinstance(item, list) for item in results):
        merged_list = []
        for item in results:
            merged_list.extend(item)
        return merged_list

    final = {}

    for result in results:
        if not isinstance(result, dict):
            continue

        for key, value in result.items():
            if value in [None, "", []]:
                continue

            if key not in final or final[key] in [None, "", []]:
                final[key] = value
                continue

            if isinstance(value, list) and isinstance(final.get(key), list):
                final[key] = list(dict.fromkeys(final[key] + value))

    return final
