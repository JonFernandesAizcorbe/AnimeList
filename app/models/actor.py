from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from app.models.user_actor import user_actor_table

class ActorORM(Base):
    __tablename__ = "actors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500))
    image: Mapped[str | None] = mapped_column(String(255))

    # Relationship Many To Many with UserORM, secondary user_actor_table
    users = relationship(
        "UserORM",
        secondary=user_actor_table,
        back_populates="actors"
    )

    # Relationship Many to Many with Anime, intermediate table AnimeActorORM
    animes: Mapped[list["AnimeActorORM"]] = relationship(
        back_populates="actor"
    )