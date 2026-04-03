from pydantic import BaseModel, ConfigDict


class GenreBase(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True
    )


class GenreCreate(BaseModel):
    name: str
