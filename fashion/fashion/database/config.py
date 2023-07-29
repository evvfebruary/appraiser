from enum import StrEnum


class InsertModes(StrEnum):
    MANY: str = "many"
    SINGLE: str = "single"


MONGO_INSERT_MODE = InsertModes.MANY
