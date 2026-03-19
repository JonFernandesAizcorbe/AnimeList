from datetime import date
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum, Integer, String, Date
from app.models.user_actor import users_actors_table

gender_enum = Enum(
    "Masculino",
    "Femenino",
    "No Binario",
    "Andrógino",
    "Género fluido",
    "Sin género",
    "Desconocido",
    "Otro",
    name="gender_enum"
)

class ActorORM(Base):
    __tablename__ = "actors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    birth: Mapped[date | None] = mapped_column(Date, nullable=True)
    gender: Mapped[str | None] = mapped_column(gender_enum, default="Desconocido", nullable=True)
    hometown: Mapped[str | None] = mapped_column(String(100), nullable=True)
    bio: Mapped[str | None] = mapped_column(String(1500), nullable=True)
    height: Mapped[int | None ] = mapped_column(Integer, nullable=True)
    image: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Relationship Many To Many with UserORM, secondary user_actor_table
    users: Mapped[list["UserORM"]] = relationship(
        "UserORM",
        secondary=users_actors_table,
        back_populates="actors"
    )

    # # Relationship Many to Many with Anime, intermediate table AnimeActorORM
    # animes: Mapped[list["AnimeActorORM"]] = relationship(
    #     back_populates="actor"
    # )


    # Many to one with CharacterORM

    character: Mapped[list["CharacterORM"]] = relationship(
        "CharacterORM",
        back_populates="actor"
    )