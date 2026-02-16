from datetime import datetime
from zoneinfo import ZoneInfo
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, Integer, String
from app.models.user_actor import user_actor_table
from app.models.user_character import user_character_table
import pytz


madrid_tz = pytz.timezone("Europe/Madrid")

class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_name: Mapped[str] = mapped_column(String(25), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500))
    image: Mapped[str | None] = mapped_column(String(500))
    create_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(madrid_tz), nullable=False)


    #Relationship Many to Many with: FriendORM
    friends_sent: Mapped[list["FriendORM"]] = relationship(
        foreign_keys="FriendORM.user_id",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    friends_received: Mapped[list["FriendORM"]] = relationship(
        foreign_keys="FriendORM.friend_id",
        back_populates="friend",
        cascade="all, delete-orphan"
    )

    #Relationship Many to Many with: Actors

    actors: Mapped[list["ActorORM"]] = relationship(
        "ActorORM",
        secondary=user_actor_table,
        back_populates="users"
    )


    #Relationship Many to Many with: Anime, intermediate table: AnimeListORM

    animes: Mapped[list["AnimeListORM"]] = relationship(
        "AnimeListORM",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    #Relationship Many to Many with: Character, intermediate table: CharacterORM

    characters: Mapped[list["CharacterORM"]] = relationship(
        "CharacterORM",
        secondary=user_character_table,
        back_populates="users"
    )