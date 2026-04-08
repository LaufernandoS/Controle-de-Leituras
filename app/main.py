from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader
import os
import datetime

from .database import engine, SessionLocal, Base
from . import models
from .routes import books as books_router

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static",
)

# Workaround Python 3.14 + Starlette 1.0: nova assinatura do TemplateResponse
# e cache do Jinja2 quebrado. Ambiente criado manualmente com cache desabilitado.
_jinja_env = Environment(
    loader=FileSystemLoader(os.path.join(BASE_DIR, "templates")),
    cache_size=0,
)
templates = Jinja2Templates(env=_jinja_env)

# Criação das tabelas 
Base.metadata.create_all(bind=engine)


# Seed: popula o banco com exemplo na primeira execução
def seed():
    db = SessionLocal()
    try:
        if db.query(models.Author).count() > 0:
            return

        autores = [
            models.Author(name="Machado de Assis",  nationality="Brasileira"),
            models.Author(name="Clarice Lispector", nationality="Brasileira"),
            models.Author(name="Graciliano Ramos",  nationality="Brasileira"),
            models.Author(name="Jorge Amado",        nationality="Brasileira"),
        ]
        db.add_all(autores)
        db.flush()

        livros = [
            models.Book(
                title="Dom Casmurro",
                total_pages=256, pages_read=256,
                start_date=datetime.date(2024, 1, 10),
                status="concluido", author_id=autores[0].id,
            ),
            models.Book(
                title="Memórias Póstumas de Brás Cubas",
                total_pages=288, pages_read=144,
                start_date=datetime.date(2024, 3, 5),
                status="lendo", author_id=autores[0].id,
            ),
            models.Book(
                title="A Hora da Estrela",
                total_pages=96, pages_read=0,
                start_date=None, status="quero_ler", author_id=autores[1].id,
            ),
            models.Book(
                title="Perto do Coração Selvagem",
                total_pages=208, pages_read=80,
                start_date=datetime.date(2024, 4, 1),
                status="lendo", author_id=autores[1].id,
            ),
            models.Book(
                title="Vidas Secas",
                total_pages=176, pages_read=176,
                start_date=datetime.date(2023, 11, 20),
                status="concluido", author_id=autores[2].id,
            ),
            models.Book(
                title="Capitães da Areia",
                total_pages=320, pages_read=0,
                start_date=None, status="quero_ler", author_id=autores[3].id,
            ),
        ]
        db.add_all(livros)
        db.commit()
        print("✅ Banco populado com dados de exemplo.")
    except Exception as e:
        db.rollback()
        print(f"⚠️  Erro no seed: {e}")
    finally:
        db.close()


seed()

# Rotas
app.include_router(books_router.router)

@app.get("/")
def index(request: Request):
    # Starlette >= 1.0: request é o primeiro argumento, context não inclui request
    return templates.TemplateResponse(request, "index.html")