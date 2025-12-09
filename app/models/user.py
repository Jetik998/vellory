from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    avatar: Mapped[str | None] = mapped_column(nullable=True)
    tasks: Mapped[list["Task"]] = relationship(back_populates="user")  # noqa: F821

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email}, hashed_password={self.hashed_password})"
