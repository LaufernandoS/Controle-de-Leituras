"""
Rotas de livros — todos os endpoints retornam HTML (fragmentos Jinja2)
para funcionar com HTMX sem recarregar a página.
"""
import datetime
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
from sqlalchemy.orm import Session
import os

from ..database import get_db
from .. import crud

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_jinja_env = Environment(
    loader=FileSystemLoader(os.path.join(BASE_DIR, "templates")),
    cache_size=0,
)
templates = Jinja2Templates(env=_jinja_env)


# Helpers 

def _parse_date(date_str: str) -> datetime.date | None:
    """Converte string 'YYYY-MM-DD' para date; retorna None se vazio."""
    try:
        return datetime.date.fromisoformat(date_str) if date_str else None
    except ValueError:
        return None


def _infer_status(pages_read: int, total_pages: int, status: str) -> str:
    """Ajusta status automaticamente se fizer sentido."""
    if pages_read >= total_pages:
        return "concluido"
    if pages_read > 0:
        return "lendo"
    return status


# GET /books

@router.get("/books", response_class=HTMLResponse)
def list_books(request: Request, query: str = "", db: Session = Depends(get_db)):
    books = crud.list_books(db, query=query)
    # Starlette >= 1.0: TemplateResponse(request, "template", context)
    return templates.TemplateResponse(
        request, "partials/book_list.html", {"books": books, "query": query}
    )


# POST /books 

@router.post("/books", response_class=HTMLResponse)
def create_book(
    request: Request,
    title:       str = Form(...),
    author:      str = Form(...),
    total_pages: int = Form(...),
    pages_read:  int = Form(0),
    start_date:  str = Form(""),
    status:      str = Form("quero_ler"),
    db: Session = Depends(get_db),
):
    status = _infer_status(pages_read, total_pages, status)
    book = crud.create_book(
        db,
        title=title,
        author_name=author,
        total_pages=total_pages,
        pages_read=pages_read,
        start_date=_parse_date(start_date),
        status=status,
    )
    return templates.TemplateResponse(
        request, "partials/book_card.html", {"book": book}
    )


#  GET /books/{id}/edit 

@router.get("/books/{book_id}/edit", response_class=HTMLResponse)
def edit_form(request: Request, book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return templates.TemplateResponse(
        request, "partials/book_edit.html", {"book": book}
    )


#  PUT /books/{id} 

@router.put("/books/{book_id}", response_class=HTMLResponse)
def update_book(
    request: Request,
    book_id: int,
    title:       str = Form(...),
    author:      str = Form(...),
    total_pages: int = Form(...),
    pages_read:  int = Form(0),
    start_date:  str = Form(""),
    status:      str = Form("quero_ler"),
    db: Session = Depends(get_db),
):
    status = _infer_status(pages_read, total_pages, status)
    book = crud.update_book(
        db,
        book_id=book_id,
        title=title,
        author_name=author,
        total_pages=total_pages,
        pages_read=pages_read,
        start_date=_parse_date(start_date),
        status=status,
    )
    if not book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return templates.TemplateResponse(
        request, "partials/book_card.html", {"book": book}
    )


#  DELETE /books/{id} 

@router.delete("/books/{book_id}", response_class=HTMLResponse)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_book(db, book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return HTMLResponse(content="", status_code=200)