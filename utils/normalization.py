ALLOWED_ENTITY_TYPES = {
    "startup",
    "investor",
    "venture_capital_fund",
    "incubator",
    "accelerator",
    "support_organization",
    "startup_directory",
    "investor_directory",
    "unknown",
}


ENTITY_TYPE_MAPPING = {
    "investisseur": "investor",
    "incubateur": "incubator",
    "accelerateur": "accelerator",
    "accélérateur": "accelerator",
    "fonds d'investissement": "venture_capital_fund",
}


LIST_FIELDS = [
    "founders",
    "investors",
    "investment_sectors",
]


def normalize_entity(entity):
    if not isinstance(entity, dict):
        return entity

    entity_type = entity.get("entity_type")

    if isinstance(entity_type, str):
        entity_type = entity_type.strip().lower()
        entity_type = ENTITY_TYPE_MAPPING.get(entity_type, entity_type)

    if entity_type not in ALLOWED_ENTITY_TYPES:
        entity_type = "unknown"

    entity["entity_type"] = entity_type

    for field in LIST_FIELDS:
        if field in entity and entity[field] is None:
            entity[field] = []

    return entity


def normalize_data(data):
    if isinstance(data, list):
        return [normalize_entity(item) for item in data]

    if isinstance(data, dict):
        return normalize_entity(data)

    return data