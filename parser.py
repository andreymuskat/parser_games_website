import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup as BS

data = pd.DataFrame(columns=['name_bg', 'link_bg', 'rating'])
FILE = 'Games.csv'
LINK = "https://tesera.ru/location/russia/moscow/wants/"

request_link = requests.get(LINK)
html = BS(request_link.content, 'html.parser')
games_items = html.select(".gameslinked > .text")

num = 0  # счетчик игр
page = 1

# while True:
while page <= 1:
    if (len(games_items)):
        for elements in games_items:
            try:
                title = elements.select('h3 > a')
                rating = elements.select('h3 > span')

                name_of_board_game = title[0].text
                link_of_board_game = str('https://tesera.ru' + title[0]['href'])
                rating_of_board_game = rating[0].text

                data.loc[num, 'name_bg'] = name_of_board_game
                data.loc[num, 'link_bg'] = link_of_board_game
                data.loc[num, 'rating'] = rating_of_board_game
            except IndexError:

                name_of_board_game = title[0].text
                link_of_board_game = str('https://tesera.ru' + title[0]['href'])
                rating_of_board_game = float('nan')

                data.loc[num, 'name_bg'] = name_of_board_game
                data.loc[num, 'link_bg'] = link_of_board_game
                data.loc[num, 'rating'] = rating_of_board_game


            num += 1
    else:
        break



    request_link = requests.get(LINK + str(page))  # проход по страницам
    html = BS(request_link.content, 'html.parser')
    games_items = html.select(".gameslinked > .text")
    page += 1

writer = pd.ExcelWriter('Game_data.xlsx')     #запись данных в excel
data.to_excel(writer)
writer.save()




