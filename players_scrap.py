import sys
import argparse
import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
from string import ascii_lowercase

def read_link(link):
    """Reads link to manipulate it with BeautifulSoup"""
    # Handles error if link is incorrect
    try:
        r = requests.get(link)
        print('link: \n', link)
    except requests.exceptions.ConnectionError:
        print('URL not valid')
        sys.exit()
    soup = BeautifulSoup(r.content, 'lxml')
    return soup


main_link = 'https://www.basketball-reference.com/'

for c in ascii_lowercase:
    pass

link_players_alphabet = main_link + 'players/' + 'a'

alphabet_letter = read_link(link_players_alphabet)

draft_table = alphabet_letter.find(class_="overthrow table_container")
body = draft_table.find("tbody").find_all("th")

def add_player_and_stats(global_list):
    name_player = player.find('a')['href']
    link_player = main_link + name_player
    player_page = read_link(link_player)
    player_name = player_page.find('div', attrs={'itemtype': 'https://schema.org/Person'}).find('h1').text
    print('player name is ', player_name)
    player_list.append(player_name)
    player_stats = player_page.find('div', attrs={'class': 'stats_pullout'})
    player_stats_p1 = player_stats.find('div', attrs={'class': 'p1'}).find_all('p')
    total_games = player_stats_p1[1].text
    total_points = player_stats_p1[3].text
    total_rebounds = player_stats_p1[5].text
    total_assists = player_stats_p1[7].text
    player_list.append(total_games)
    player_list.append(total_points)
    player_list.append(total_rebounds)
    player_list.append(total_assists)
    print(player_list)

player_list = []
for player in body:
    add_player_and_stats(player_list)
updated_player_list = [player_list[x:x + 5] for x in range(0, len(player_list), 5)]
player_df = pd.DataFrame(player_list, columns=['name_player',
                                               'total_games_played',
                                               'total_points',
                                               'total_rebounds',
                                               'total_assists'
                                               ''])

engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                           .format(user="root",
                                   pw="pwdmysql",
                                   db="basketball"))
player_df.to_sql('players', con=engine, if_exists='append', chunksize=1000, index=False)



