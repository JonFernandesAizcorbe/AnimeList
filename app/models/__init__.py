"""
Modelos de base de datos (SQLALchemy)
"""

from app.models.user import UserORM
from app.models.anime import AnimeORM
from app.models.friend import FriendORM
from app.models.user_actor import users_actors_table
from app.models.anime_genre import animes_genres_table
from app.models.actor import ActorORM
# from app.models.anime_actor import AnimeActorORM
from app.models.anime_list import AnimeListORM, display_status
from app.models.genre import GenreORM
from app.models.user_character import users_characters_table
from app.models.anime_character import animes_characters_table

__all__ = ["UserORM", "AnimeORM", "FriendORM", "users_actors_table", "animes_genres_table", "ActorORM", "AnimeListORM", "GenreORM", "users_characters_table", "display_status", "animes_characters_table"]