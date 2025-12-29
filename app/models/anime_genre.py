from sqlalchemy import Column, ForeignKey, Integer, Table

from app.database import Base


animes_genres_table = Table(
    "animes_genres",
    Base.metadata,
    Column("anime_id", Integer, ForeignKey("animes.id"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id"), primary_key=True),
)
