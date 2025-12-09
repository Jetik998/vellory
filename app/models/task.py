from datetime import datetime
from sqlalchemy import ForeignKey
from app.utils import time
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


# Таблица задачи
class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    # deadline: Mapped[datetime | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=time)
    completed: Mapped[bool] = mapped_column(default=False)
    priority: Mapped[int] = mapped_column(default=0)
    user: Mapped["User"] = relationship(back_populates="tasks")  # noqa: F821

    def __repr__(self):
        return f"Task(id={self.id}, title={self.title}, description={self.description}, created_at={self.created_at}, completed={self.completed}, priority={self.priority})"
