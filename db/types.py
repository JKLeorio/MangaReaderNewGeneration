from enum import Enum


class Role(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"


class TranslateStatus(str, Enum):
    NOT_TRANSLATED = "Not translated"
    IN_PRODUCTION = "In production"
    FROZEN = "Frozen"
    TRANSLATED = "Translated"


class ReleaseStatus(str, Enum):
    RELEASED = "Released"
    IN_PRODUCTION = "In production"
    FROZEN = "Frozen"

class ImageExtensions(str, Enum):
    pass

class UserLIbraryItemStatus(str, Enum):
    READING = "Reading"
    IN_PLANS = "In plans"
    ABANDONED = "Abandoned"
    FAVORITE = "Favorite"


class ComicTypes(str, Enum):
    #Не полный список
    MANGA = "Manga"
    MANHWA = "Manhwa"
    COMIC = "Comic"
    MANHUA = "Manhua"
    OEL_MANGA = "Oel manga"