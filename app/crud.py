"""
Operações de banco de dados — sem lógica HTTP aqui.
As rotas chamam estas funções e não tocam no DB diretamente.
"""
from sqlalchemy.orm import Session
from sqlalchemy import or_
from . import models


# Autores 

def get_or_create_author(db: Session, name: str) -> models.Author:
    """Retorna o autor pelo nome ou cria um novo se não existir."""
    author = db.query(models.Author).filter(
        models.Author.name.ilike(name.strip())
    ).first()
    if not author:
        author = models.Author(name=name.strip())
        db.add(author)
        db.flush()  # gera o ID sem commitar
    return author


def list_authors(db: Session) -> list[models.Author]:
    return db.query(models.Author).order_by(models.Author.name).all()


# Livros 

def create_book(
    db: Session,
    title: str,
    author_name: str,
    total_pages: int,
    pages_read: int,
    start_date,
    status: str = "quero_ler",
) -> models.Book:
    author = get_or_create_author(db, author_name)
    book = models.Book(
        title=title.strip(),
        total_pages=total_pages,
        pages_read=pages_read,
        start_date=start_date,
        status=status,
        author_id=author.id,
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def list_books(db: Session, query: str = "") -> list[models.Book]:
    """Lista todos os livros; filtra por título ou autor se query for informada."""
    q = db.query(models.Book).join(models.Author)
    if query:
        pattern = f"%{query.strip()}%"
        q = q.filter(
            or_(
                models.Book.title.ilike(pattern),
                models.Author.name.ilike(pattern),
            )
        )
    return q.order_by(models.Book.id.desc()).all()


def get_book(db: Session, book_id: int) -> models.Book | None:
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def update_book(
    db: Session,
    book_id: int,
    title: str,
    author_name: str,
    total_pages: int,
    pages_read: int,
    start_date,
    status: str,
) -> models.Book | None:
    book = get_book(db, book_id)
    if not book:
        return None
    author = get_or_create_author(db, author_name)
    book.title       = title.strip()
    book.author_id   = author.id
    book.total_pages = total_pages
    book.pages_read  = pages_read
    book.start_date  = start_date
    book.status      = status
    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, book_id: int) -> bool:
    book = get_book(db, book_id)
    if not book:
        return False
    db.delete(book)
    db.commit()
    return True