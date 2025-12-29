from datetime import date, datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String

from app.database import Base

display_status = Enum(
    "Viendo",
    "Completado",
    "Dropeado",
    "Proximamente",
    name = "display_status"
)


class AnimeListORM(Base):
    __tablename__ = "anime_lists"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    anime_id: Mapped[int] = mapped_column(ForeignKey("animes.id"), primary_key=True)
    comment: Mapped[str | None] = mapped_column(String(500))
    date_start: Mapped[datetime | None] = mapped_column(DateTime)
    date_end: Mapped[datetime | None] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(display_status, default="Viendo", nullable=False)
    score: Mapped[int | None] = mapped_column(Integer)

    user: Mapped["UserORM"] = relationship(back_populates="animes")
    anime: Mapped["AnimeORM"] = relationship(back_populates="users")