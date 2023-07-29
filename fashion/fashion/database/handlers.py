from collections import abc
from typing import Any


def insert_many(
    item_as_dict: dict[Any, Any],
    *,
    buffer: abc.MutableSequence[dict[Any, Any]],
    mongo_db,
    mongo_collection: str,
    buffer_size: int = 10
):
    if len(buffer) != buffer_size:
        buffer.append(item_as_dict)
    else:
        mongo_db[mongo_collection].insert_many(buffer)
        buffer.clear()


def insert_one(
    item_as_dict: dict[Any, Any], *, mongo_db, mongo_collection: str
):
    mongo_db[mongo_collection].insert_one(item_as_dict)
