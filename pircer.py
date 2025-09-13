from bs4 import BeautifulSoup
from time import sleep
from category import category_parser

import pandas as pd
import requests

data = []

def parse_recept_page(url_page):
    url = url_page
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    calories = soup.select_one('span[itemprop="calories"]').text
    protein = soup.select_one('span[itemprop="proteinContent"]').text
    fats = soup.select_one('span[itemprop="fatContent"]').text
    carbohydrate = soup.select_one('span[itemprop="carbohydrateContent"]').text
    return [calories,protein,fats,carbohydrate]

quantity_of_page = int(input("Введите количество страниц: "))

category = int(input('''ВЫберите категорию:\n
1.  Завтраки  2.  Бульоны         3.  Закуски
4.  Напитки   5.  Основные блюда  6.  Паста и пицца
7.  Ризотто   8.  Салаты          9.  Соусы и Маринады
10. Супы      11. Сэндвичи        12. Выпечка и десерты
              13. Все подряд\n'''))

for page in range(1,quantity_of_page+1):
    
    url = f"{category_parser(category)}?page={page}"
    response = requests.get(url)
    sleep(2)
    soup = BeautifulSoup(response.text, 'html.parser')
    elements = soup.find_all('div', class_="css-m0u77r")
    
    for element in elements:
        name = element.find('span',class_="css-1bs2jj2").text
        author = element.find('span', class_="css-14tqfr").text
        portions = element.find('span', class_="css-tqfyce").text
        time = element.find('span', class_="css-14gsni6").text
        url_page = "https://eda.ru"+element.find('a', class_="css-18hxz5k").get('href')
        cpfc = parse_recept_page(url_page)
        data.append([name,author, portions, time, *cpfc])

header = ['name', 'author', 'portions', 'time', 'calories', 'protein', 'fats', 'carbohydrate']

df = pd.DataFrame(data, columns=header)
df.to_csv(r'C:\Users\user\Desktop\parser\eda_data.csv', sep=';', encoding='UTF-8-sig')
