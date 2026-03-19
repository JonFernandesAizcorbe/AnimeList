

from sqlalchemy import Column, ForeignKey, Integer, Table

from app.database import Base


animes_characters_table = Table(
    "animes_characters",
    Base.metadata,
    Column("anime_id", Integer, ForeignKey("animes.id"), primary_key=True),
    Column("character_id", Integer, ForeignKey("characters.id"), primary_key=True)
)