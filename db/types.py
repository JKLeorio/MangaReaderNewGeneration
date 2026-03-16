from enum import Enum


class Role(str, Enum):
    ADMIN = "Admin"
    USER = "User"


class TranslateStatus(str, Enum):
    NOT_TRANSLATED = "Not_translated" 
    IN_PRODUCTION = "In_production"
    FROZEN = "Frozen"
    TRANSLATED = "Translated"


class ReleaseStatus(str, Enum):
    RELEASED = "Released"
    IN_PRODUCTION = "In_production"
    FROZEN = "Frozen"

class ImageExtensions(str, Enum):
    pass

class UserLIbraryItemStatus(str, Enum):
    READING = "Reading"
    IN_PLANS = "In_plans"
    ABANDONED = "Abandoned"
    FAVORITE = "Favorite"


class ComicType(str, Enum):
    #Не полный список
    MANGA = "Manga"
    MANHWA = "Manhwa"
    COMIC = "Comic"
    MANHUA = "Manhua"
    OEL_MANGA = "Oel_manga"


class CommentRefers(str, Enum):
    PERSON = "Person"
    PAGE = "Page"
    COMIC = "Comic"
