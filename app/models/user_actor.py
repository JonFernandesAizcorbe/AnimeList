from sqlalchemy import Column, ForeignKey, Integer, Table
from app.database import Base


users_actors_table = Table(
    "users_actors",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("actor_id", Integer, ForeignKey("actors.id"), primary_key=True)
)