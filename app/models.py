from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Author(Base):
    __tablename__ = "authors"

    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String(150), nullable=False, unique=True)
    nationality = Column(String(100), default="Brasileira")

    # Um autor tem muitos livros
    books = relationship("Book", back_populates="author")

    def __repr__(self):
        return f"<Author id={self.id} name={self.name!r}>"


class Book(Base):
    __tablename__ = "books"

    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String(200), nullable=False)
    total_pages = Column(Integer, nullable=False)
    pages_read  = Column(Integer, default=0)
    start_date  = Column(Date, nullable=True)
    status      = Column(String(20), default="quero_ler")
    # status pode ser: "quero_ler" | "lendo" | "concluido"

    # Foreign key para Author (relação N:1)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)

    # Muitos livros pertencem a um autor
    author = relationship("Author", back_populates="books")

    @property
    def progress(self) -> int:
        """Percentual de leitura calculado em tempo real."""
        if self.total_pages and self.total_pages > 0:
            return min(int((self.pages_read / self.total_pages) * 100), 100)
        return 0

    def __repr__(self):
        return f"<Book id={self.id} title={self.title!r} progress={self.progress}%>"