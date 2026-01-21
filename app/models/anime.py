from sqlalchemy import Integer, String
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.anime_genre import animes_genres_table



class AnimeORM(Base):
    __tablename__ = "animes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    studio: Mapped[str | None] = mapped_column(String(30))
    description: Mapped[str | None] = mapped_column(String(1000))
    num_caps: Mapped[int | None] = mapped_column(Integer)
    image: Mapped[str | None] = mapped_column(String(500))
    color: Mapped[str | None] = mapped_column(String(50))


    # Relationship Many to Many with Genre, secondary table animes_genres_table

    genres = relationship(
        "GenreORM",
        secondary=animes_genres_table,
        back_populates="animes"
    )

    # Relationship Many to Many with ActorORM, intermediate table AnimeActorORM
    actors: Mapped[list["AnimeActorORM"]] = relationship(
        back_populates="anime",
        cascade="all, delete-orphan"
    )

    # Relationship Many to Many with User, intermediate table AnimeListORM

    users: Mapped[list["AnimeListORM"]] = relationship(
        "AnimeListORM",
        back_populates="anime"
    )