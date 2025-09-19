

from typing import Any, Dict


def conditions_generator(
    model: Any,
    filters: Dict,
):
    conditions = list()
    for key, value in filters.items():
        field = getattr(model, key, None)
        if field is None:
            raise KeyError(f"{field} in model {model} doesn't exists")
        conditions.append(field == value)
    return conditions
