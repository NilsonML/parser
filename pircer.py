import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep 

data = []

def parse_by_class(url, class_name):
    for page in range(1,3):
        
        url = f"https://eda.ru/recepty?page={page}"
        response = requests.get(url)
        sleep(3)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        elements = soup.find_all('div', class_=class_name)
        
        for element in elements:
            name = element.find('span',class_="css-1bs2jj2").text
            author = element.find('span', class_="css-14tqfr").text
            portions = element.find('span', class_="css-tqfyce").text
            time = element.find('span', class_="css-14gsni6").text
            data.append([name,author, portions, time])
    return data
        
url = "https://eda.ru/recepty?page=1"

header = ['name', 'author', 'portions', 'time']

df = pd.DataFrame(parse_by_class(url,"css-m0u77r"), columns=header)
df.to_csv(r'C:\Users\user\Desktop\parser\eda_data.csv', sep=';', encoding='UTF-8-sig')
