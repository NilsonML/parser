"""
eda_parser.py — сбор рецептов с eda.ru: название, автор, порции, время и КБЖУ.

Запуск:
    python eda_parser.py                       # спросит категорию и число страниц
    python eda_parser.py -c 8 -p 3 -o salads.csv
"""

import argparse
import time
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://eda.ru"

# Номер -> (название, slug в URL). Словарь вместо match/case: его легко
# вывести в меню, проверить номер и дополнить новой категорией.
CATEGORIES = {
    1: ("Завтраки", "zavtraki"),
    2: ("Бульоны", "bulony"),
    3: ("Закуски", "zakuski"),
    4: ("Напитки", "napitki"),
    5: ("Основные блюда", "osnovnye-blyuda"),
    6: ("Паста и пицца", "pasta-picca"),
    7: ("Ризотто", "rizotto"),
    8: ("Салаты", "salaty"),
    9: ("Соусы и маринады", "sousy-marinady"),
    10: ("Супы", "supy"),
    11: ("Сэндвичи", "sendvichi"),
    12: ("Выпечка и десерты", "vypechka-deserty"),
    13: ("Все подряд", ""),
}

HEADERS = {"User-Agent": "Mozilla/5.0 (recipe-parser; educational project)"}
DELAY_SECONDS = 2      # пауза между запросами: не нагружаем сайт
TIMEOUT_SECONDS = 15   # без таймаута один зависший ответ вешает весь скрипт
COLUMNS = ["name", "author", "portions", "time", "calories", "protein", "fats", "carbohydrate"]


def category_url(number: int) -> str:
    if number not in CATEGORIES:
        raise ValueError(f"Нет категории {number}. Доступны: 1–{len(CATEGORIES)}")
    slug = CATEGORIES[number][1]
    return f"{BASE_URL}/recepty/{slug}".rstrip("/")


def fetch(session: requests.Session, url: str) -> BeautifulSoup:
    response = session.get(url, headers=HEADERS, timeout=TIMEOUT_SECONDS)
    response.raise_for_status()
    time.sleep(DELAY_SECONDS)
    return BeautifulSoup(response.text, "html.parser")


def text_of(element, selector_kwargs: dict) -> str | None:
    """Текст дочернего элемента или None, если его нет (вёрстка бывает разной)."""
    found = element.find(**selector_kwargs) if element else None
    return found.get_text(strip=True) if found else None


def parse_nutrition(soup: BeautifulSoup) -> list[str | None]:
    """КБЖУ со страницы рецепта. У части рецептов КБЖУ нет — тогда None, а не падение."""
    values = []
    for prop in ("calories", "proteinContent", "fatContent", "carbohydrateContent"):
        tag = soup.select_one(f'span[itemprop="{prop}"]')
        values.append(tag.get_text(strip=True) if tag else None)
    return values


def parse_category(category: int, pages: int) -> pd.DataFrame:
    rows = []
    with requests.Session() as session:  # одно TCP-соединение на все запросы (keep-alive)
        for page in range(1, pages + 1):
            soup = fetch(session, f"{category_url(category)}?page={page}")
            cards = soup.find_all("div", class_="css-m0u77r")
            print(f"Страница {page}: {len(cards)} рецептов")
            for card in cards:
                link = card.find("a", class_="css-18hxz5k")
                if link is None:
                    continue
                recipe_soup = fetch(session, BASE_URL + link.get("href"))
                rows.append([
                    text_of(card, {"name": "span", "class_": "css-1bs2jj2"}),
                    text_of(card, {"name": "span", "class_": "css-14tqfr"}),
                    text_of(card, {"name": "span", "class_": "css-tqfyce"}),
                    text_of(card, {"name": "span", "class_": "css-14gsni6"}),
                    *parse_nutrition(recipe_soup),
                ])
    return pd.DataFrame(rows, columns=COLUMNS)


def ask_category() -> int:
    for number, (title, _) in CATEGORIES.items():
        print(f"{number:>2}. {title}")
    return int(input("Выберите категорию: "))


def main() -> None:
    parser = argparse.ArgumentParser(description="Парсер рецептов eda.ru")
    parser.add_argument("-c", "--category", type=int, help="номер категории (1–13)")
    parser.add_argument("-p", "--pages", type=int, help="сколько страниц каталога обойти")
    parser.add_argument("-o", "--output", type=Path, default=Path("eda_data.csv"))
    args = parser.parse_args()

    category = args.category or ask_category()
    pages = args.pages or int(input("Введите количество страниц: "))

    df = parse_category(category, pages)
    df.to_csv(args.output, sep=";", index=False, encoding="utf-8-sig")
    print(f"Сохранено {len(df)} рецептов в {args.output}")


if __name__ == "__main__":
    main()
