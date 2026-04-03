from typing import Set
from fastapi import HTTPException, status

from ..base_service import BaseService

from models.comic import Comic
from models.genre import Genre
from schemas.genre import GenreCreate


class GenreService(BaseService):
    model = Genre

    async def create(
        self,
        genre_data: GenreCreate
    ):
        genre_dump = genre_data.model_dump()
        new_genre = Genre(
            **genre_dump
        )
        self._session.add(new_genre)
        await self._session.flush()
        return new_genre
    
    async def get_genres(self):
        genres = await self.get_all()
        return genres

    async def bind_comic_genres(
        self,
        comic_record: Comic,
        genres_ids: Set[int]
    ):
        genres = await self.get_all(
            Genre.id.in_(genres_ids)
        )
        
        if len(genres) != len(genres_ids):
            raise HTTPException(
                detail="Fill genres with exist ids",
                status_code=status.HTTP_404_NOT_FOUND
            )
        comic_record.genres = genres
        await self._session.flush()