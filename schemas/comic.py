from typing import Annotated, List, Optional
from fastapi import File, Form, UploadFile
from pydantic import BaseModel
from fastapi_filter.contrib.sqlalchemy import Filter
from db.types import ComicType, ReleaseStatus, TranslateStatus
from models.comic import Comic, ComicGenre
from schemas.cover import CoverResponse
from schemas.genre import GenreBase
from schemas.pagination import Pagination
from schemas.person import PersonBase, PersonResponse


class ComicBase(BaseModel):
    id: int
    title: str
    type: ComicType
    description: str
    release_date: int
    author_id: int
    artist_id: int
    release_status: ReleaseStatus
    translate_status: TranslateStatus

class ComicResponse(BaseModel):
    id: int
    title: str
    type: ComicType
    release_date: int
    description: str
    author: PersonResponse
    artist: PersonResponse
    cover_url: str
    genres: Optional[List["GenreBase"]] = []
    # covers: list[CoverResponse]
    release_status: ReleaseStatus
    translate_status: TranslateStatus




class ComicsPaginated(BaseModel):
    comics: List[ComicResponse]
    pagination: Pagination


class ComicPartialUpdate(BaseModel):
    title: Optional[str] = None
    type: Optional[ComicType] = None
    description: Optional[str] = None
    release_date: Optional[int] = None
    author_id: Optional[int] = None
    artist_id: Optional[int] = None
    release_status: ReleaseStatus
    translate_status: TranslateStatus


class ComicCreate(BaseModel):
    title: str
    description: Optional[str] = None
    type: ComicType = ComicType.MANGA
    release_date: int
    author_id: int | None = None
    artist_id: int | None = None
    release_status: ReleaseStatus = ReleaseStatus.IN_PRODUCTION
    translate_status: TranslateStatus = TranslateStatus.IN_PRODUCTION
    genres: Optional[List["GenreBase"]] = []

    @classmethod
    def as_form(
        cls,
        title: Annotated[str, Form()],
        type: Annotated[ComicType, Form()],
        release_date: Annotated[int, Form()],
        description: Annotated[str | None, Form()] = None,
        author_id: Annotated[int | None, Form()] = None,
        artist_id: Annotated[int | None, Form()] = None,
    ) -> "ComicCreate":
        return cls(
            title=title,
            type=type,
            description=description,
            release_date=release_date,
            author_id=author_id,
            artist_id=artist_id,
        )




class ChapterBase(BaseModel):
    id: int
    title: str
    comic_id: int
    position: int
    volume: int


class ChapterResponse(BaseModel):
    id: int
    title: str
    comic: ComicBase
    position: int
    volume: int

class ChapterWithPagesResponse(ChapterResponse):
    pages: List["PageBase"]

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
    # image_id: int
    image_url: str
    

class PageResponse(BaseModel):
    id: int
    position: int
    chapter_id: int
    image_url: str

class PageCreate(BaseModel):
    position: int
    chapter_id: int
    # image_id: int
    image_url: str

    @classmethod
    def as_form(
        cls,
        position: Annotated[int, Form()],
        chapter_id: Annotated[int, Form()],
        image_url: Annotated[str, Form()],
    ) -> "ComicCreate":
        return cls(
            position=position,
            chapter_id=chapter_id,
            image_url=image_url
        )


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

