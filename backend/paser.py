import httpx
from bs4 import BeautifulSoup
import pandas as pd
from pymystem3 import Mystem

page = httpx.get('https://ru.wikipedia.org/wiki/100_%D1%81%D0%B0%D0%BC%D1%8B%D1%85_%D0%B2%D0%BB%D0%B8%D1%8F%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D1%85_%D0%BB%D1%8E%D0%B4%D0%B5%D0%B9_%D0%B2_%D0%B8%D1%81%D1%82%D0%BE%D1%80%D0%B8%D0%B8_(%D0%BA%D0%BD%D0%B8%D0%B3%D0%B0)')
soup = BeautifulSoup(page.text)
parsed_professions = [el.contents[0] for el in soup.find_all('td', attrs={'align': 'left'})]

parsed = soup.find_all('td', attrs={'align': 'center'})
parsed_names = list()
for element in parsed:
    row = element.find_all('a')
    if len(row) > 0:
        row = row[0].contents[0]
        if not (row.isdigit() or 'н. э.' in row or 'год' in row):
            parsed_names.append(row)

names = list()
surnames = list()
professions = list()
for i in range(len(parsed_names)):
    name, *surname = parsed_names[i].split()
    surname = ' '.join(surname)
    profession = parsed_professions[i]
    if len(profession) > 64:
        profession = profession[:62] + '...'

    if len(name) > 64:
        name = name[:62] + '...'

    if len(surname) > 64:
        surname = surname[:62] + '...'

