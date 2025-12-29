from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from app.models.anime_genre import animes_genres_table

class GenreORM(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    description: Mapped[str | None] = mapped_column(String(500))


    # Relationship Many to Many with AnimeORM, secondary table animes_genres_table

    animes = relationship(
        "AnimeORM",
        secondary=animes_genres_table,
        back_populates="genres"
    )