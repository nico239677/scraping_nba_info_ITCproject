import sys
import argparse
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from functions import *
from sqlalchemy import create_engine

with open('database_config.py', "rb") as source_file:
    code = compile(source_file.read(), 'database_config.py', "exec")
exec(code)

# Parsing years of the data to scrap
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

draft_list = []
for year in range(FIRST_YEAR, LAST_YEAR+1):
    link_draft = main_link + 'draft/NBA_' + str(year) + '.html'

    draft = read_link(link_draft)

    print('LIST OF ALL DRAFTS FOR YEAR ', year)
    draft_table = draft.find(class_="overthrow table_container")
    body = draft_table.find("tbody").find_all("td")

    for draft in body:
        # Adding player info
        add_tag_link_and_year(draft_list, draft, 'play-index', year)

        # Adding player name: need to do a if statement,
        # since player name usually is within a <a> tag,
        # sometimes directly in a class tag without link
        if 'players' in str(draft.find('a')):
            element = draft.find('a').text
            draft_list.append(element)
        elif 'data-stat="player"' in str(draft):
            element = draft.text
            draft_list.append(element)

        # Adding player stats
        add_text_in_tag(draft_list, draft, 'data-stat="g"')
        add_text_in_tag(draft_list, draft, 'data-stat="mp"')
        add_text_in_tag(draft_list, draft, 'data-stat="pts"')
        add_text_in_tag(draft_list, draft, 'data-stat="trb"')
        add_text_in_tag(draft_list, draft, 'data-stat="ast"')

        add_text_in_tag(draft_list, draft, 'data-stat="mp_per_g"')
        add_text_in_tag(draft_list, draft, 'data-stat="pts_per_g"')
        add_text_in_tag(draft_list, draft, 'data-stat="trb_per_g"')
        add_text_in_tag(draft_list, draft, 'data-stat="ast_per_g"')

    # Turning the list into list of lists
updated_draft_list = [draft_list[x:x + 12] for x in range(0, len(draft_list), 12)]

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

#  Filling tables line by line
cursor = connection.cursor()

cols = ", ".join([str(i) for i in draft_df.columns.tolist()])
for i, row in draft_df.iterrows():
    cursor.execute("INSERT IGNORE INTO drafts ( " + cols + ") VALUES (" + "%s,"*(len(row)-1) + "%s)", tuple(row))

# Deleting duplicates
cursor.execute("DROP TABLE IF EXISTS drafts_no_duplicates")
cursor.execute("CREATE TABLE drafts_no_duplicates SELECT DISTINCT year,"
               "number_draft,"
               "name,"
               "number_of_games,"
               "total_minutes_played,"
               "total_points,"
               "total_rebounds,"
               "total_assists,"
               "minutes_per_game,"
               "points_per_game,"
               "rebounds_per_game, assists_per_game "
               "FROM drafts")
cursor.execute("DROP TABLE drafts")
cursor.execute("ALTER TABLE drafts_no_duplicates RENAME TO drafts")

connection.commit()


# Filling table if empty
# engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
#                        .format(user="root",
#                                pw="pwdmysql",
#                                db="basketball"))
# draft_df.to_sql('drafts', con=engine, if_exists='append', chunksize=1000, index=False)

# print('\n\n\n----------\n\n\n')

# print('BONUS')

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
#           row.td.nextSibling.nextSibling.text if row.td.nextSibling.nextSibling.text else "N/A", ' win, ',
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
