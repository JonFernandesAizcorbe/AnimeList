from pydantic import BaseModel, ConfigDict, field_validator


class ActorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    image: str | None

class ActorCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: str | None = None
    image: str | None = None

    @field_validator("name")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        
        return v.strip()
    
    @field_validator("description")
    @classmethod
    def not_empty_or_none(cls, v: str | None) -> str | None:
        if v is None or not v.strip():
            return None
        
        return v.strip()
    
class ActorPatch(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str | None = None
    description: str | None = None
    image: str | None = None

    @field_validator("name", "description")
    @classmethod
    def not_empty_or_none(cls, v: str | None) -> str | None:
        if v is None or not v.strip():
            return None
        
        return v.strip()