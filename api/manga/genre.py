from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_async_session
from models.genre import ComicGenre
from schemas.genre import ComicGenreBase, ComicGenreCreate, GenreBase, GenreCreate
from services.comic.genre_service import GenreService


genre_router = APIRouter()


@genre_router.get(
    '/',
    response_model=List[GenreBase],
    status_code=status.HTTP_200_OK
)
async def get_genres(
    session: AsyncSession = Depends(get_async_session)
):
    genre_service = GenreService(
        session=session
    )
    genres = await genre_service.get_genres()
    return genres

@genre_router.post(
    '/',
    response_model=List[GenreBase],
    status_code=status.HTTP_201_CREATED
)
async def create_genre(
    genre_create_data: GenreCreate,
    session: AsyncSession = Depends(get_async_session),
):
    genre_service = GenreService(
        session=session
    )
    new_genre = await genre_service.create(
        genre_create_data
    )
    await genre_service.refresh(
        new_genre
    )
    return new_genre


