from sqlalchemy import Enum, ForeignKey, Integer, String
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.user_character import users_characters_table
from app.models.anime_character import animes_characters_table

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


class CharacterORM(Base):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    age: Mapped[str | None]  = mapped_column(String(50), nullable=True)
    gender: Mapped[str] = mapped_column(gender_enum, default="Desconocido", nullable=False)
    bio: Mapped[str | None] = mapped_column(String(1500), nullable=True)
    image: Mapped[str] = mapped_column(String(250), nullable=False)
    actor_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("actors.id"))
    


    # Relatinoship many to many with: CharacterORM, intermediate table: user_charater_table
    users: Mapped[list["UserORM"]] = relationship(
        "UserORM",
        secondary=users_characters_table,
        back_populates="characters"
    )

    # Relationship one to many with: ActorORM
    actor: Mapped["ActorORM"] = relationship(
        "ActorORM",
        back_populates="character"
    )

    # Relationship one to many with: AnimeORM
    animes: Mapped[list["AnimeORM"]] = relationship(
        "AnimeORM",
        secondary=animes_characters_table,
        back_populates="characters"
    )