from sqlalchemy.orm import Mapped, mapped_column, MappedColumn
from database import Base

class BookModel(Base):
    __tablename__ = "books"

    id: Mapped[int] = MappedColumn(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]
    year: Mapped[int | None]
    read: Mapped[bool] = MappedColumn(default=False)
    rating: Mapped[int | None]