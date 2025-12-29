from pydantic import BaseModel, ConfigDict, field_validator


class GenreResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None


class GenreCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: str | None = None

    @field_validator("name")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("El nombre del Anime no puede estar vacío")
        
        return v.strip()
    
    @field_validator("description")
    @classmethod
    def not_empty_or_none(cls, v: str | None) -> str | None:
        if v is None or not v.strip():
            return None
        
        return v.strip()
    
class GenrePatch(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str | None = None
    description: str | None = None
    
    @field_validator("name", "description")
    @classmethod
    def not_empty_or_none(cls, v: str | None) -> str | None:
        if v is None or not v.strip():
            return None
        
        return v.strip()