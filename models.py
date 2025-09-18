from datetime import datetime
from moscow_time import moscow_time
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True
    pass

#Таблица задачи
class Task(Base):
    __tablename__ = 'task'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=moscow_time)
    completed: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        return f"Task(id={self.id}, title={self.title}, description={self.description}, created_at={self.created_at}, completed={self.completed})"

