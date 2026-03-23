from typing import Any, Dict, Iterable
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


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



async def validate_ids(
        session: AsyncSession,
        models_ids: Dict[Any, Iterable[int]],
        ignore_None: bool = True
        ):
    for model, ids in models_ids.items():
        for id in ids:
            if ignore_None and id is None:
                continue
            if (await session.get(model, id)) is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"{model.__name__} with id {id} not found"
                )