import json


def parse_llm_json(response):
    if not response:
        return None

    response = response.strip()
    response = response.replace("```json", "")
    response = response.replace("```", "")
    response = response.strip()

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        start_array = response.find("[")
        start_object = response.find("{")

        starts = [
            index for index in [start_array, start_object]
            if index != -1
        ]

        if not starts:
            print("Reponse LLM sans JSON valide :")
            print(response[:1000])
            return None

        start = min(starts)
        end_array = response.rfind("]")
        end_object = response.rfind("}")

        end = max(end_array, end_object)

        if end == -1 or end <= start:
            print("JSON probablement coupe par le modele.")
            print(response[:1000])
            return None

        json_text = response[start:end + 1]

        try:
            return json.loads(json_text)
        except json.JSONDecodeError as error:
            print("Erreur JSON apres nettoyage :")
            print(error)
            print(json_text[:1000])
            return None


def merge_entities(results):
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