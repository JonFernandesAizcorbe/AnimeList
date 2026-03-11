"""
Modelos de base de datos (SQLALchemy)
"""

from app.models.user import UserORM
from app.models.anime import AnimeORM
from app.models.friend import FriendORM
from app.models.user_actor import user_actor_table
from app.models.anime_genre import animes_genres_table
from app.models.actor import ActorORM
# from app.models.anime_actor import AnimeActorORM
from app.models.anime_list import AnimeListORM, display_status
from app.models.genre import GenreORM
from app.models.user_character import user_character_table

__all__ = ["UserORM", "AnimeORM", "FriendORM", "user_actor_table", "animes_genres_table", "ActorORM", "AnimeListORM", "GenreORM", "user_character_table", "display_status"]