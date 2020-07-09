import sys
import argparse
import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
from string import ascii_lowercase
from tqdm import tqdm
import string
import re

# with open('database_config.py', "rb") as source_file:
#     code = compile(source_file.read(), 'database_config.py', "exec")
# exec(code)

parser = argparse.ArgumentParser()
parser.add_argument('-first',
                    '--start_letter',
                    type=str,
                    default='a',
                    help='choose first year of data to scrap')
parser.add_argument('-last',
                    '--end_letter',
                    type=str,
                    default='z',
                    help='choose last year of data to scrap')
args = parser.parse_args()


def read_link(link):
    """Reads link to manipulate it with BeautifulSoup"""
    # Handles error if link is incorrect
    try:
        r = requests.get(link)
        # print('link: \n', link)
    except requests.exceptions.ConnectionError:
        print('URL not valid')
        sys.exit()
    soup = BeautifulSoup(r.content, 'lxml')
    return soup


def add_player_and_stats(global_list):
    name_player = player.find('a')['href']
    link_player = main_link + name_player
    player_page = read_link(link_player)
    player_name = player_page.find('div', attrs={'itemtype': 'https://schema.org/Person'}).find('h1').text
    player_list.append(player_name)
    # print('player name is ', player_name)
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


main_link = 'https://www.basketball-reference.com/'

letters = string.ascii_lowercase
FIRST_LETTER = args.start_letter.lower()
LAST_LETTER = args.end_letter.lower()

# Checking that FIRST_LETTER and LAST_LETTER are alphabet letters
try:
    assert (FIRST_LETTER.isalpha())
    assert (LAST_LETTER.isalpha())
except AssertionError:
    print("Please enter a valid letter")
    sys.exit()


print('pattern is ', FIRST_LETTER +'(.*)'+ LAST_LETTER)
range_alphabet = re.search(FIRST_LETTER + '(.*)' + LAST_LETTER, letters).group(1)
range_alphabet = letters[letters.find(FIRST_LETTER): letters.find(LAST_LETTER)]
print('tring is ', range_alphabet)

# Scrap all players whose last name starts with a letter between FIRST_LETTER and LAST_LETTER
player_list = []
for char in range_alphabet:
    print(char)
    link_players_alphabet = main_link + 'players/' + char
    alphabet_letter = read_link(link_players_alphabet)
    draft_table = alphabet_letter.find(class_="overthrow table_container")
    body = draft_table.find("tbody").find_all("th")
    for player in tqdm(body):
        add_player_and_stats(player_list)
updated_player_list = [player_list[x:x + 5] for x in range(0, len(player_list), 5)]
player_df = pd.DataFrame(updated_player_list, columns=['name_player',
                                                       'number_of_games_career',
                                                       'total_points_career',
                                                       'total_rebounds_career',
                                                       'total_assists_career'])


engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="pwdmysql",
                               db="basketball"))
player_df.to_sql('players', con=engine, if_exists='append', chunksize=1000, index=False)



