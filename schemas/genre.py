from pydantic import BaseModel, ConfigDict


class GenreBase(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True
    )


class GenreCreate(BaseModel):
    name: str




class ComicGenreBase(BaseModel):
    comic_id: int
    genre_id: int


class ComicGenreCreate(BaseModel):
    comic_id: int
    genre_id: int