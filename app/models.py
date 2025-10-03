from datetime import datetime

from sqlalchemy import ForeignKey

from app.utils import time
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    __abstract__ = True
    pass


# Таблица задачи
class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=time)
    completed: Mapped[bool] = mapped_column(default=False)
    user: Mapped["User"] = relationship(back_populates="tasks")

    def __repr__(self):
        return f"Task(id={self.id}, title={self.title}, description={self.description}, created_at={self.created_at}, completed={self.completed})"


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    tasks: Mapped[list["Task"]] = relationship(back_populates="user")

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email}, hashed_password={self.hashed_password})"
