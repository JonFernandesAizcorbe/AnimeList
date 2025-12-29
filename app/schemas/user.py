from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_name: str
    email: EmailStr
    password: str
    description: str | None
    image: str | None
    create_at: datetime


class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_name: str
    email: EmailStr
    password: str
    description: str | None = None
    image: str | None = None

    @field_validator("user_name")
    @classmethod
    # validate user_name is not empty
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        
        return v.strip()
    
    @field_validator("email")
    @classmethod
    # validate temporals mails
    def is_email(cls, v: EmailStr) -> EmailStr:
        if v.endswith("@tempmail.com"):
            raise ValueError("No puede ser un correo temporal")
        
        return v
    
    @field_validator("password")
    @classmethod
    # validate password len is >= 8
    def len_pass(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("La contraseña tiene que tener un mínimo de 8 carácteres")
        
        return v
    
    @field_validator("description")
    @classmethod
    def len_description(cls, v: str | None) -> str | None:
        if v is not None and len(v) > 500:
            raise ValueError("La descripción no puede tener más de 500 carácteres")
        
        return v
    
class UserPatch(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    description: str | None
    image: str | None
    create_at: datetime | None

    @field_validator("user_name")
    @classmethod
    # validate user_name is not empty
    def not_empty(cls, v: str | None) -> str | None:

        if v is None:
            return None
        
        if not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        
        return v.strip()

    @field_validator("email")
    @classmethod
    # validate temporals mails
    def is_email(cls, v: EmailStr | None) -> EmailStr | None:
        if v is not None and v.endswith("@tempmail.com"):
            raise ValueError("No puede ser un correo temporal")
        
        return v

    @field_validator("password")
    @classmethod
    # validate password len is >= 8
    def len_pass(cls, v: str | None) -> str | None:
        if v is not None and len(v) < 8:
            raise ValueError("La contraseña tiene que tener un mínimo de 8 carácteres")
        
        return v
    
    @field_validator("description")
    @classmethod
    def len_description(cls, v: str | None) -> str | None:
        if v is not None and len(v) > 500:
            raise ValueError("La descripción no puede tener más de 500 carácteres")
        
        return v