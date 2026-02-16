from pydantic import BaseModel, ConfigDict, field_validator

# ANIME RESPONSE
class AnimeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    studio: str | None
    description: str | None
    num_caps: int | None
    image: str | None
    banner: str | None
    color: str | None

# ANIME CREATE
class AnimeCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    studio: str | None = None
    description: str | None = None
    num_caps: int | None = None
    image: str | None = None
    banner: str | None = None
    color: str | None = None

    @field_validator("name")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        
        return v.strip()
    
    @field_validator("studio","description")
    @classmethod
    def not_empty_or_none(cls, v: str | None) -> str | None:
        if v is None or not v.strip():
            return None
        
        return v.strip()
    
    @field_validator("num_caps")
    @classmethod
    def real_num_or_none(cls, v: int | None) -> int | None:
        if v is None:
            return None
        
        if v < 0:
            raise ValueError("El número de capítulos tiene que ser un número positivo")
        
        return v
    
# ANIME PATCH
class AnimePatch(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str | None = None
    description: str | None = None
    num_caps: int | None = None
    image: str | None = None

    @field_validator("name", "description")
    @classmethod
    def not_empty_or_none(cls, v: str | None) -> str | None:
        if v is None or not v.strip():
            return None
        
        return v.strip()
    
    @field_validator("num_caps")
    @classmethod
    def not_real_or_none(cls, v: int | None) -> int | None:
        if v is None:
            return None
        
        if v < 0:
            raise ValueError("El número de capítulos tiene que ser un número positivo")

        return v


        
