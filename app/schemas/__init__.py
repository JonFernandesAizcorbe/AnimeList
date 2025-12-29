"""
Esquemas Pydantic para validacion de datos
"""
from app.schemas.user import UserResponse, UserCreate, UserPatch
from app.schemas.anime import AnimeResponse, AnimeCreate, AnimePatch
from app.schemas.genre import GenreResponse, GenreCreate , GenrePatch
from app.schemas.actor  import ActorResponse, ActorCreate, ActorPatch

__all__ = ["UserResponse",
            "UserCreate",
            "UserPatch",
            "AnimeResponse",
            "AnimeCreate",
            "AnimePatch",
            "GenreResponse",
            "GenreCreate",
            "GenrePatch",
            "ActorResponse",
            "ActorCreate",
            "ActorPatch"
        ]