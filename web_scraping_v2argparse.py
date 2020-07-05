import sys
import argparse
import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

with open('create_table.py', "rb") as source_file:
    code = compile(source_file.read(), 'create_table.py', "exec")
exec(code)

# Parsing years of data to scrap
parser = argparse.ArgumentParser()
parser.add_argument('-first',
                    '--start_year',
                    type=int,
                    default=2010,
                    help='choose first year of data to scrap')
parser.add_argument('-last',
                    '--end_year',
                    type=int,
                    default=datetime.today().year-1,
                    help='choose last year of data to scrap')
args = parser.parse_args()


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


def add_tag_link_and_year(global_list, string, year_draft):
    if string in str(draft.find('a')):
        element = draft.find('a').text if draft.find('a').text else None
        global_list.append(year_draft)
        global_list.append(element)
        return


def add_tag_link(global_list, string):
    if string in str(draft.find('a')):
        element = draft.find('a').text if draft.find('a').text else None
        global_list.append(element)
        return


def add_tag_text_in_tag(global_list, string):
    if string in str(draft):
        element = draft.text if draft.text else None
        global_list.append(element)


main_link = 'https://www.basketball-reference.com/'

# Getting the data of all drafts for a specific period of time
FIRST_YEAR = args.start_year
LAST_YEAR = args.end_year

# Checking that last year comes after first year
try:
    assert (LAST_YEAR >= FIRST_YEAR)
except AssertionError:
    print("Last year to scrap should be higher than first year")
    sys.exit()

for year in range(FIRST_YEAR, LAST_YEAR+1):
    print('year is ', year)
    link_draft = main_link + 'draft/NBA_' + str(year) + '.html'

    draft = read_link(link_draft)

    print('LIST OF ALL DRAFTS FOR YEAR ', year)
    draft_table = draft.find(class_="overthrow table_container")
    body = draft_table.find("tbody").find_all("td")

    draft_list = []
    for draft in body:
        # Adding player info
        add_tag_link_and_year(draft_list, 'play-index', year)

        # add_tag_link(draft_list, 'players')
        if 'players' in str(draft.find('a')):
            element = draft.find('a').text
            draft_list.append(element)
            #if draft.find('a').text
        elif 'data-stat="player"' in str(draft):
            element = draft.text
            draft_list.append(element)

        add_tag_text_in_tag(draft_list, 'data-stat="g"')
        add_tag_text_in_tag(draft_list, 'data-stat="mp"')
        add_tag_text_in_tag(draft_list, 'data-stat="pts"')
        add_tag_text_in_tag(draft_list, 'data-stat="trb"')
        add_tag_text_in_tag(draft_list, 'data-stat="ast"')

        add_tag_text_in_tag(draft_list, 'data-stat="mp_per_g"')
        add_tag_text_in_tag(draft_list, 'data-stat="pts_per_g"')
        add_tag_text_in_tag(draft_list, 'data-stat="trb_per_g"')
        add_tag_text_in_tag(draft_list, 'data-stat="ast_per_g"')

    # print('draft_list is ', draft_list)

    # Turning the list into list of lists
    updated_draft_list = [draft_list[x:x + 12] for x in range(0, len(draft_list), 12)]
    name = 'list_draft_' + str(year) + '.csv'

    # Storing the data in dataframe and exporting it to CSV
    draft_df = pd.DataFrame(updated_draft_list, columns=['year',
                                                         'number_draft',
                                                         'name',
                                                         'number_of_games',
                                                         'total_minutes_played',
                                                         'total_points',

                                                         'total_rebounds',
                                                         'total_assists',
                                                         'minutes_per_game',
                                                         'points_per_game',
                                                         'rebounds_per_game',

                                                         'assists_per_game'
                                                         ''])
    # print(draft_df)
    # draft_df.to_csv(name)
    engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                           .format(user="root",
                                   pw="pwdmysql",
                                   db="basketball"))
    draft_df.to_sql('players', con=engine, if_exists='append', chunksize=1000, index=False)


print('\n\n\n----------\n\n\n')

# Get global stats from main page
# print("\nRESULTS OF THE YEAR SO FAR")
#
# main = read_link(main_link)
# score_file = main.find("div", attrs={'class': "data_grid section_wrapper"})
# table_list = score_file.find_all('div', attrs={'class': "table_wrapper"})
#
# for table in table_list:
#     all_rows = table.find_all("tr", attrs={'class': 'full_table'})
#     break
# scores = []
# for row in all_rows:
#     print(row.a['title'] if row.a['title'] else "N/A", ' : ',
#           row.td.nextSibling.nextSibling.text if row.td.nextSibling.nextSibling.text else "N/A", ' wins, ',
#           row.td.nextSibling.nextSibling.nextSibling.text if row.td.nextSibling.nextSibling.nextSibling.text\
# else "N/A", 'losses')
#
#     # Adding data to file, and making sure it exists
#     info = [row.a['title'] if row.a['title'] else "N/A",
#             row.td.nextSibling.nextSibling.text if row.td.nextSibling.nextSibling.text else "N/A",
#             row.td.nextSibling.nextSibling.nextSibling.text if row.td.nextSibling.nextSibling.nextSibling.text \
# else "N/A"]
#     scores.append(info)
# scores_df = pd.DataFrame(scores, columns=['team', 'wins', 'losses'])
# scores_df.to_csv('scores.csv')
#
# print('\n\n LAST SCORES\n')
# scores = main.find('div', attrs={'class': 'game_summaries'})
# games = scores.find_all('table', attrs={'class': 'teams'})
# last_games = []
# for game in games:
#     loser = game.find('tr', attrs={'class': 'loser'}).find('a').text
#     score_loser = game.find('tr', attrs={'class': 'loser'}).find('td', attrs={'class': 'right'}).text
#     winner = game.find('tr', attrs={'class': 'winner'}).find('a').text
#     score_winner = game.find('tr', attrs={'class': 'winner'}).find('td', attrs={'class': 'right'}).text
#     print(winner, ' won to ', loser, ' with a score of ', score_winner, ' to ', score_loser)
#
#     # Adding data to a csv file
#     info_games = [winner if winner else "N/A",
#                   loser if loser else "N/A",
#                   score_winner if score_winner else "N/A",
#                   score_loser if score_loser else "N/A"]
#     last_games.append(info_games)
# last_games_df = pd.DataFrame(last_games, columns=['Winner', 'Loser', 'Score winner', 'Score loser'])
# last_games_df.to_csv('last_games.csv')
#
# print('\n\nCURRENT TRENDING PLAYERS\n')
# news = main.find('div', attrs={'id': 'current'})
# trending_players = news.find('div').nextSibling.find_all("a")
# for player in trending_players:
#     print(player.text)
#
# print('\n\nLAST NEWS - RUMORS\n')
# rumors = news.find('div').nextSibling.nextSibling.nextSibling.find_all('li')
# for rumor in rumors:
#     print(rumor.text, 'available at the link: ', rumor.a['href'])
