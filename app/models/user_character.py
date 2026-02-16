

from sqlalchemy import Column, ForeignKey, Integer, Table

from app.database import Base


user_character_table = Table(
    "user_characters",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("actor_id", Integer, ForeignKey("characters.id"), primary_key=True)
)