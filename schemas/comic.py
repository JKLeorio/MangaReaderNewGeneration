from typing import Optional
from pydantic import BaseModel

from db.types import ComicType
from schemas.cover import CoverResponse
from schemas.person import PersonBase, PersonResponse


class ComicBase(BaseModel):
    id: int
    title: str
    type: ComicType
    release_date: int
    author_id: int
    artist_id: int

class ComicResponse(BaseModel):
    id: int
    title: str
    type: ComicType
    release_date: int
    author: PersonResponse
    artist: PersonResponse
    covers: list[CoverResponse]

class ComicCreate(BaseModel):
    title: str
    type: ComicType
    release_date: int
    author_id: Optional[int] = None
    artist_id: Optional[int] = None



class ChapterBase(BaseModel):
    id: int
    title: str
    comic_id: int
    position: int
    volume: int


class ChapterResponse(BaseModel):
    id: int
    title: str
    comic: ChapterBase
    position: int
    volume: int

class ChapterCreate(BaseModel):
    title: str
    comic_id: int
    position: int
    volume: int

class ChapterPartialUpdate(BaseModel):
    title: Optional[str] = None
    comic_id: Optional[int] = None
    position: Optional[int] = None
    volume: Optional[int] = None


class PageBase(BaseModel):
    id: int
    position: int
    chapter_id: int
    image_id: int

class PageResponse(BaseModel):
    id: int
    position: int
    chapter_id: int
    image_url: str

class PageCreate(BaseModel):
    position: int
    chapter_id: int
    image_id: int

class PagePartialUpdate(BaseModel):
    position: Optional[int] = None
    chapter_id: Optional[int] = None
    image_id: Optional[int] = None