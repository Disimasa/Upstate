# import httpx
# from bs4 import BeautifulSoup
# import pandas as pd
# from pymystem3 import Mystem
#
# page = httpx.get('https://ru.wikipedia.org/wiki/100_%D1%81%D0%B0%D0%BC%D1%8B%D1%85_%D0%B2%D0%BB%D0%B8%D1%8F%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D1%85_%D0%BB%D1%8E%D0%B4%D0%B5%D0%B9_%D0%B2_%D0%B8%D1%81%D1%82%D0%BE%D1%80%D0%B8%D0%B8_(%D0%BA%D0%BD%D0%B8%D0%B3%D0%B0)')
# soup = BeautifulSoup(page.text)
# parsed_professions = [el.contents[0] for el in soup.find_all('td', attrs={'align': 'left'})]
#
# parsed = soup.find_all('td', attrs={'align': 'center'})
# parsed_names = list()
# for element in parsed:
#     row = element.find_all('a')
#     if len(row) > 0:
#         row = row[0].contents[0]
#         if not (row.isdigit() or 'н. э.' in row or 'год' in row):
#             parsed_names.append(row)
#
#
# names = list()
# surnames = list()
# professions = list()
# for i in range(len(parsed_names)):
#     name, *surname = parsed_names[i].split()
#     if len(surname) > 0:
#         if 'I' in surname[0] or 'X' in surname[0] or 'V' in surname[0]:
#             name += ' ' + surname[0]
#             if len(surname) > 1:
#                 surname = surname[1:]
#             else:
#                 surname = ''
#     surname = ' '.join(surname)
#     profession = parsed_professions[i]
#     max_length = 16
#     if len(profession) > max_length:
#         profession = profession[:max_length-3].strip() + '...'
#
#     if len(name) > max_length:
#         name = name[:max_length-3].strip() + '...'
#
#     if len(surname) > max_length:
#         surname = surname[:max_length-3].strip() + '...'
#
#     name = name.strip('\n').strip(',')
#     surname = surname.strip('\n')
#     try:
#         profession = profession.strip('\n')
#     except:
#         continue
#
#     names.append(name)
#     surnames.append(surname)
#     professions.append(profession)
#
# names = pd.Series(names, name='name')
# surnames = pd.Series(surnames, name='surname')
# professions = pd.Series(professions, name='profession')
# res = pd.concat([names, surnames, professions], axis=1)
# res.to_csv('persons.csv', index=False)


import pandas as pd
data = pd.read_csv('persons.csv')
data['profession'] = data['profession'].apply(lambda x: x[:13]+'...' if len(x) > 16 else x)
data.to_csv('persons2.csv', index=False)
