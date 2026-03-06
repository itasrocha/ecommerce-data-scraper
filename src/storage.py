"""
Módulo de Armazenamento — SQLAlchemy
Define o modelo da tabela e salva o DataFrame no PostgreSQL.
"""

import logging
from datetime import datetime, timezone

import pandas as pd
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.orm import DeclarativeBase

logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    availability = Column(String, nullable=False)
    scraped_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    def __repr__(self) -> str:
        return f"<Book(title='{self.title}', price={self.price}, category='{self.category}')>"

def get_engine(database_url: str):
    """Cria engine SQLAlchemy a partir da URL de conexão."""
    engine = create_engine(database_url, echo=False)
    return engine


def create_tables(engine):
    """Cria as tabelas no banco se não existirem."""
    Base.metadata.create_all(engine)
    logger.info("Tabelas criadas/verificadas com sucesso")


def save_to_db(df: pd.DataFrame, engine) -> int:
    """
    Salva o DataFrame no banco de dados.
    Adiciona timestamp de coleta automaticamente.
    Retorna o número de registros inseridos.
    """
    df = df.copy()
    df["scraped_at"] = datetime.now(timezone.utc)

    rows = df.to_sql(
        name="books",
        con=engine,
        if_exists="append",
        index=False,
    )

    logger.info("Inseridos %d registros na tabela 'books'", rows if rows else len(df))
    return rows if rows else len(df)
