import argparse
import pandas as pd
from tqdm import tqdm
import string
from functions import *

NUMBER_SCRAPED_COLUMNS = 5

with open('database_config.py', "rb") as source_file:
    code = compile(source_file.read(), 'database_config.py', "exec")
exec(code)

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


# def add_player_and_stats(row_player, global_list):
#     name_player = row_player.find('a')['href']
#     link_player = main_link + name_player
#     player_page = read_link(link_player)
#     player_name = player_page.find('div', attrs={'itemtype': 'https://schema.org/Person'}).find('h1').text
#     global_list.append(player_name)
#     print('player name is ', player_name)
#     player_stats = player_page.find('div', attrs={'class': 'stats_pullout'})
#     player_stats_p1 = player_stats.find('div', attrs={'class': 'p1'}).find_all('p')
#     total_games = player_stats_p1[1].text
#     total_points = player_stats_p1[3].text
#     total_rebounds = player_stats_p1[5].text
#     total_assists = player_stats_p1[7].text
#     global_list.append(total_games)
#     global_list.append(total_points)
#     global_list.append(total_rebounds)
#     global_list.append(total_assists)


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

range_alphabet = letters[letters.find(FIRST_LETTER): letters.find(LAST_LETTER) + 1]

# Scrap all players whose last name starts with a letter between FIRST_LETTER and LAST_LETTER
player_list = []
for char in range_alphabet:
    print('Scraping all players whose last name starts with ', char, '...')
    link_players_alphabet = main_link + 'players/' + char
    alphabet_letter = read_link(link_players_alphabet)
    draft_table = alphabet_letter.find(class_="overthrow table_container")
    try:
        body = draft_table.find("tbody").find_all("th")
    except AttributeError:
        print('Link not valid')
        continue
    for player in tqdm(body):
        # add_player_and_stats(player, player_list)
        name_player = player.find('a')['href']
        link_player = main_link + name_player
        player_page = read_link(link_player)
        player_name = player_page.find('div', attrs={'itemtype': 'https://schema.org/Person'}).find('h1').text
        player_list.append(player_name)
        print('player name is ', player_name)
        player_stats = player_page.find('div', attrs={'class': 'stats_pullout'})
        player_stats_p1 = player_stats.find('div', attrs={'class': 'p1'}).find_all('p')
        total_games = player_stats_p1[1].text
        total_points = player_stats_p1[3].text
        total_rebounds = player_stats_p1[5].text
        total_assists = player_stats_p1[7].text

        arr_per_game = player_page.find('div', attrs={'class': "overthrow table_container", 'id': 'div_per_game'})
        body_per_game = arr_per_game.find('tbody').find_all('tr')
        for row in body_per_game:
            try:
                year = row.find('a').text[:-3]
                # print('year is ', year)
                team = row.find('td', attrs={'data-stat': 'team_id'})
                try:
                    name_team = team.find('a').text
                except:
                    name_team = team.text
                print(name_team)
            except:
                pass
            player_list.append(year)
            player_list.append(name_team)
            player_list.append(total_games)
            player_list.append(total_points)
            player_list.append(total_rebounds)
            player_list.append(total_assists)

# Turning the list into list of lists
updated_player_list = [player_list[x:x + NUMBER_SCRAPED_COLUMNS]
                       for x in range(0, len(player_list), NUMBER_SCRAPED_COLUMNS)]

# Storing the data in dataframe and exporting it to database
player_df = pd.DataFrame(updated_player_list, columns=['year_played',
                                                       'team_year',
                                                       'name_player',
                                                       'number_of_games_career',
                                                       'total_points_career',
                                                       'total_rebounds_career',
                                                       'total_assists_career'])


#  Filling tables line by line
cursor = connection.cursor()

cols = ", ".join([str(i) for i in player_df.columns.tolist()])
for i, row in player_df.iterrows():
    cursor.execute("INSERT IGNORE INTO players ( " + cols + ") VALUES (" + "%s," * (len(row) - 1) + "%s)", tuple(row))

# Deleting duplicates
# cursor.execute("DROP TABLE IF EXISTS players_no_duplicates")
# cursor.execute("CREATE TABLE players_no_duplicates SELECT DISTINCT name_player,"
#                "number_of_games_career,"
#                "total_points_career,"
#                "total_rebounds_career,"
#                "total_assists_career "
#                "FROM players")
# cursor.execute("DROP TABLE players")
# cursor.execute("ALTER TABLE players_no_duplicates RENAME TO players")
#
# connection.commit()

# engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
#                        .format(user="root",
#                                pw="pwdmysql",
#                                db="basketball"))
# player_df.to_sql('players', con=engine, if_exists='append', chunksize=1000, index=False)
