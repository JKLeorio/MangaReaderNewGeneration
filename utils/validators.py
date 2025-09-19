from typing import Dict



def dict_comparator(
        received: Dict, 
        extended: Dict,
        key_matching: bool = True
        ) -> bool:
    """
    Compare two dicts
    """
    for key, value in received.items():
        ex_value = extended.get(key, None)
        if (ex_value is None):
            if key_matching is True:
                raise KeyError(f"key {key} doesn't exist in expected")
            continue
        if ex_value != value:
            return False
    return True