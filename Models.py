from sqlalchemy.orm import DeclarativeBase, relationship, mapped_column, Mapped
from sqlalchemy import ForeignKey, String, Date
from typing import List

class Base(DeclarativeBase):
    pass

class User(Base):
    """
    username:str
    password:str
    email:str
    """
    __tablename__ = "User"
    id:Mapped[int] = mapped_column(primary_key=True)
    username:Mapped[str] = mapped_column(String(30))
    password:Mapped[str] = mapped_column(String())
    email:Mapped[str] = mapped_column(String(30))
    words:Mapped[List["Words"]] = relationship(back_populates="user")


class Words(Base):
    """
    user_id:int
    word:str
    time_posted:str
    """
    __tablename__ = "Word"
    id:Mapped[int] = mapped_column(primary_key=True)
    word:Mapped[str]
    time_posted:Mapped[str] = mapped_column(Date)
    user_id = mapped_column(ForeignKey("User.id"))
    user:Mapped[User] = relationship(back_populates="words")
