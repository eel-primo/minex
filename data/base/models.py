from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True, index=True)
    is_blocked = Column(Boolean, default=False)

    servers = relationship("Servers", back_populates="owner")


class Servers(Base):
    __tablename__ = "servers"

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String, index=True)
    title = Column(String, index=True)
    note = Column(String, index=True)
    last_online = Column(Integer, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="servers")