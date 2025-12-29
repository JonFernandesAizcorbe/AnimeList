from sqlalchemy import ForeignKey, Integer, String
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class AnimeActorORM(Base):
    __tablename__ = "anime_actors"

    anime_id: Mapped[int] = mapped_column(ForeignKey("animes.id"), primary_key=True)
    actor_id: Mapped[int] = mapped_column(ForeignKey("actors.id"), primary_key=True)
    character: Mapped[str | None] = mapped_column(String(150))
    language: Mapped[str | None] = mapped_column(String(100))

    # relationship with anime, actors

    anime: Mapped["AnimeORM"] = relationship(back_populates="actors")
    actor: Mapped["ActorORM"] = relationship(back_populates="animes")