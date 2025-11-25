from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from settings import Base


# Модель Note
class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    done: Mapped[bool] = mapped_column(default=False)

    def __str__(self):
        return f"Нотатка з {self.id} та {self.name}"
