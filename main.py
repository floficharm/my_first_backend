from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import BookModel

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Create_book(BaseModel):
    title: str
    author: str
    year: int | None = None
    rating: int | None = Field(default=None, ge=1, le=5)


class Book(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    author: str
    year: int | None = None
    read: bool
    rating: int | None = Field(default=None, ge=1, le=5)


class Update_book(BaseModel):
    title: str | None = None
    author: str | None = None
    year: int | None = None
    read: bool | None = None
    rating: int | None = Field(default=None, ge=1, le=5)


def find_book(id_book: int, db: Session) -> BookModel:
    book = db.get(BookModel, id_book)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.get("/books", response_model=list[Book])
def get_book(db: Session = Depends(get_db)):
    return db.query(BookModel).order_by(BookModel.id).all()


@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(data: Create_book, db: Session = Depends(get_db)):
    book = BookModel(
        title=data.title,
        author=data.author,
        year=data.year,
        rating=data.rating,
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@app.patch("/books/{id_book}", response_model=Book)
def update_book(id_book: int, data: Update_book, db: Session = Depends(get_db)):
    book = find_book(id_book, db)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(book, field, value)
    db.commit()
    db.refresh(book)
    return book


@app.delete("/books/{id_book}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(id_book: int, db: Session = Depends(get_db)):
    book = find_book(id_book, db)
    db.delete(book)
    db.commit()