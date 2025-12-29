from pydantic import BaseModel, ConfigDict


class AnimeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    num_caps: int | None
    image: str | None


class AnimeCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: str | None
    num_caps: int | None
    image: str | None
