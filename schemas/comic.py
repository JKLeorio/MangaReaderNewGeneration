from typing import Annotated, List, Optional
from fastapi import File, Form, UploadFile
from pydantic import BaseModel
from fastapi_filter.contrib.sqlalchemy import Filter
from db.types import ComicType
from models.comic import Comic
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
    cover_url: str
    # covers: list[CoverResponse]

class ComicCreate(BaseModel):
    title: str
    type: ComicType
    release_date: int
    author_id: Optional[int] = None
    artist_id: Optional[int] = None

class ComicPartialUpdate(BaseModel):
    title: Optional[str] = None
    type: Optional[ComicType] = None
    release_date: Optional[int] = None
    author_id: Optional[int] = None
    artist_id: Optional[int] = None


class ComicCreateForm(BaseModel):
    def __init__(
            self,
            title: Annotated[str, Form()],
            type: Annotated[ComicType, Form()],
            release_date: Annotated[int, Form()],
            cover: UploadFile,
            author_id: Annotated[int, Form()] = None,
            artist_id: Annotated[int, Form()] = None,
            ):
        self.title = title
        self.type = type
        self.release_date = release_date
        self.cover = cover
        self.author_id = author_id
        self.artist_id = artist_id




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



class ComicFilter(Filter):
    title: Optional[str] = None
    type__in: Optional[List[ComicType]] = None
    release_date: Optional[int] = None

    class Constants(Filter.Constants):
        model = Comic