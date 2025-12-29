from datetime import UTC, datetime, timezone
from enum import Enum
from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


friend_status_enum = Enum(
    "Pendiente",
    "Acceptado",
    "Bloqueado",
    "Rechazado",
    name="friend_status"
)

class FriendORM(Base):
    __tablename__ = "friends"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    friend_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)

    status: Mapped[str] = mapped_column(friend_status_enum, default="Pendiente", nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))


    # Relationship Many to Many with UserORM
    user: Mapped["UserORM"] = relationship(
        foreign_keys=[user_id],
        back_populates="friends_sent"
    )

    friend: Mapped["UserORM"] = relationship(
        foreign_keys=[friend_id],
        back_populates="friends_received"     
    )



















    
    # user: Mapped["UserORM"] = relationship(
    #     foreign_keys=[user_id],
    #     back_populates="friends_sent"
    # )

    # friend: Mapped["UserORM"] = relationship(
    #     foreign_keys=[friend_id],
    #     back_populates="friends_received"
    # )