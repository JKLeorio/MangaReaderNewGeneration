from typing import List

from utils.validators import validate_ids

from ..base_service import BaseService

from models.comic import Comic
from models.genre import ComicGenre, Genre
from schemas.genre import ComicGenreCreate, GenreCreate


class GenreService(BaseService):
    model = Genre

    async def create(
        self,
        genre_data: GenreCreate
    ):
        new_genre = Genre(
            **genre_data
        )
        self._session.add(new_genre)
        await self._session.flush()
        return new_genre
    
    async def get_genres(self):
        genres = await self.get_all()
        return genres


class ComicGenresService(BaseService):
    model = ComicGenre

    fk_fields_on_create = {
        Comic: ["comic_id"],
        Genre : ["genre_id"]
    }

    async def create(
        self,
        comic_genres_data: ComicGenreCreate
    ):
        await self.validate_ids(
            comic_genres_data
        )
        new_comic_genre = ComicGenre(
            **comic_genres_data
        )
        self._session.add(
            new_comic_genre
        )
        await self._session.flush()
        return new_comic_genre
    

    async def bind_comic_genres(
        self,
        comic_id: int,
        genres_ids: List[int]
    ):
        models_ids = {
            Comic : [comic_id],
            Genre: genres_ids
        }
        await validate_ids(
            self._session,
            models_ids=models_ids
        )
        comic_genres = []
        for genre_id in genres_ids:
            comic_genre = ComicGenre(
                comic_id=comic_id,
                genre_id=genre_id
            )
            comic_genres.append(comic_genre)
            self._session.add(comic_genre)
        await self._session.flush()