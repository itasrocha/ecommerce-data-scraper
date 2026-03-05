"""
Módulo de Coleta — Selenium + XPath
Navega pelo catálogo do Books to Scrape por categoria,
extraindo dados de cada livro usando seletores XPath.
"""

import logging
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)

BASE_URL = "https://books.toscrape.com/"

XPATH_CATEGORY_LINKS = "//div[@class='side_categories']//ul/li/ul/li/a"
XPATH_PRODUCT_CARDS = "//article[@class='product_pod']"
XPATH_TITLE = "./h3/a/@title"
XPATH_PRICE = ".//p[@class='price_color']"
XPATH_RATING_CLASS = "./p[contains(@class,'star-rating')]"
XPATH_AVAILABILITY = ".//p[contains(@class,'availability')]"
XPATH_NEXT_PAGE = "//li[@class='next']/a"


def _create_driver() -> webdriver.Chrome:
    """Cria instância do Chrome headless para scraping."""
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1920,1080")

    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=opts)
    driver.implicitly_wait(0)
    return driver


def _extract_rating(card) -> str:
    """Extrai o texto da avaliação (One, Two, ...) a partir da classe CSS."""
    rating_el = card.find_element(By.XPATH, XPATH_RATING_CLASS)
    classes = rating_el.get_attribute("class")
    parts = classes.split()
    return parts[1] if len(parts) > 1 else "Zero"


def _scrape_category_page(driver, category: str) -> list[dict]:
    """Extrai livros de uma única página dentro de uma categoria."""
    books = []
    cards = driver.find_elements(By.XPATH, XPATH_PRODUCT_CARDS)

    for card in cards:
        title_el = card.find_element(By.XPATH, "./h3/a")
        title = title_el.get_attribute("title")

        price_el = card.find_element(By.XPATH, XPATH_PRICE)
        price = price_el.text

        rating = _extract_rating(card)

        avail_el = card.find_element(By.XPATH, XPATH_AVAILABILITY)
        availability = avail_el.text.strip()

        books.append(
            {
                "title": title,
                "price": price,
                "category": category,
                "rating": rating,
                "availability": availability,
            }
        )

    return books


def _scrape_category(driver, category_url: str, category_name: str) -> list[dict]:
    """Navega por todas as páginas de uma categoria e coleta os livros."""
    all_books = []
    driver.get(category_url)
    time.sleep(1)

    while True:
        books = _scrape_category_page(driver, category_name)
        all_books.extend(books)
        logger.info(
            "  Página coletada: %d livros (total categoria: %d)",
            len(books),
            len(all_books),
        )

        try:
            next_btn = driver.find_element(By.XPATH, XPATH_NEXT_PAGE)
            next_url = next_btn.get_attribute("href")
            driver.get(next_url)
            time.sleep(0.5)
        except Exception:
            break

    return all_books


def scrape_all() -> list[dict]:
    """
    Ponto de entrada principal do scraper.
    Coleta todos os livros de todas as categorias.
    Retorna lista de dicts com dados brutos.
    """
    driver = _create_driver()
    all_books = []

    try:
        logger.info("Acessando %s", BASE_URL)
        driver.get(BASE_URL)

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, XPATH_CATEGORY_LINKS))
        )

        cat_elements = driver.find_elements(By.XPATH, XPATH_CATEGORY_LINKS)
        categories = []
        for el in cat_elements:
            name = el.text.strip()
            url = el.get_attribute("href")
            categories.append((name, url))

        logger.info("Encontradas %d categorias", len(categories))

        for i, (cat_name, cat_url) in enumerate(categories, 1):
            logger.info("[%d/%d] Categoria: %s", i, len(categories), cat_name)
            books = _scrape_category(driver, cat_url, cat_name)
            all_books.extend(books)

        logger.info("Coleta finalizada: %d livros no total", len(all_books))

    finally:
        driver.quit()

    return all_books
