"""
Pipeline de Monitoramento de Preços — Books to Scrape

Orquestrador principal que executa as três etapas:
1. Coleta (Selenium + XPath)
2. Processamento (Pandas)
3. Armazenamento (SQLAlchemy + PostgreSQL)
"""

import logging
import os
import sys
import time

from scraper import scrape_all
from processor import process
from storage import get_engine, create_tables, save_to_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)-12s | %(message)s",
    datefmt="%H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("pipeline")


def main():
    start = time.time()
    logger.info("=" * 60)
    logger.info("INÍCIO DO PIPELINE DE MONITORAMENTO DE PREÇOS")
    logger.info("=" * 60)

    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql://scraper:scraper123@localhost:5432/books_db",
    )
    engine = get_engine(database_url)
    create_tables(engine)

    logger.info("-" * 40)
    logger.info("ETAPA 1: Coleta de dados (Selenium + XPath)")
    logger.info("-" * 40)
    raw_data = scrape_all()
    logger.info("Dados brutos coletados: %d registros", len(raw_data))

    if not raw_data:
        logger.error("Nenhum dado coletado. Abortando pipeline.")
        sys.exit(1)

    logger.info("-" * 40)
    logger.info("ETAPA 2: Processamento (Pandas)")
    logger.info("-" * 40)
    df = process(raw_data)
    logger.info("DataFrame processado: %d linhas, %d colunas", *df.shape)

    logger.info("-" * 40)
    logger.info("ETAPA 3: Armazenamento (SQLAlchemy → PostgreSQL)")
    logger.info("-" * 40)
    rows_saved = save_to_db(df, engine)

    elapsed = time.time() - start
    logger.info("=" * 60)
    logger.info("PIPELINE CONCLUÍDO COM SUCESSO")
    logger.info("  Livros coletados:  %d", len(raw_data))
    logger.info("  Livros salvos:     %d", rows_saved)
    logger.info("  Categorias:        %d", df["category"].nunique())
    logger.info("  Preço médio:       £%.2f", df["price"].mean())
    logger.info("  Rating médio:      %.1f ★", df["rating"].mean())
    logger.info("  Tempo total:       %.1f segundos", elapsed)
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
