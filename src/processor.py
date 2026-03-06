"""
Módulo de Processamento — Pandas
Limpa e transforma os dados brutos coletados pelo scraper.
"""

import logging
import re

import pandas as pd

logger = logging.getLogger(__name__)

RATING_MAP = {
    "Zero": 0,
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


def process(raw_data: list[dict]) -> pd.DataFrame:
    """
    Recebe lista de dicts com dados brutos e retorna
    um DataFrame limpo e tipado.
    """
    df = pd.DataFrame(raw_data)
    logger.info("DataFrame criado com %d linhas", len(df))

    df["price"] = (
        df["price"]
        .str.replace("£", "", regex=False)
        .str.replace("Â", "", regex=False)
        .str.strip()
        .astype(float)
    )
    logger.info("Preços convertidos para float")

    df["rating"] = df["rating"].map(RATING_MAP).fillna(0).astype(int)
    logger.info("Avaliações convertidas para inteiro")

    df["availability"] = df["availability"].str.strip()
    logger.info("Disponibilidade normalizada")

    df["category"] = df["category"].str.strip()

    logger.info("Processamento concluído")
    logger.info(
        "Resumo — Preço médio: £%.2f | Categorias: %d | Rating médio: %.1f",
        df["price"].mean(),
        df["category"].nunique(),
        df["rating"].mean(),
    )

    return df
