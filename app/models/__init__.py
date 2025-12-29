"""
Modelos de base de datos (SQLALchemy)
"""

from app.models.user import UserORM
from app.models.anime import AnimeORM
from app.models.friend import FriendORM
from app.models.user_actor import user_actor_table
from app.models.anime_genre import animes_genres_table
from app.models.actor import ActorORM
from app.models.anime_actor import AnimeActorORM
from app.models.anime_list import AnimeListORM
from app.models.genre import GenreORM

__all__ = ["UserORM", "AnimeORM", "FriendORM", "user_actor_table", "animes_genres_table", "ActorORM", "AnimeActorORM", "AnimeListORM", "GenreORM"]