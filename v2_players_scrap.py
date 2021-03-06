from gevent import monkey as curious_george
curious_george.patch_all(thread=False, select=False)
from parser_file import *
import grequests
import pandas as pd
from tqdm import tqdm
from functions import *
from variables import *
from api_nba import get_info_draft_api


with open('database_config.py', "rb") as source_file:
    code = compile(source_file.read(), 'database_config.py', "exec")
exec(code)

cur = connection.cursor()

# Scrap all players whose last name starts with a letter between FIRST_LETTER and LAST_LETTER
player_list = []

link_lists = []

# for movie_list in list_urls:
#     rs = [grequests.get(u) for u in movie_list]
#     results = grequests.map(rs)

for char in range_alphabet:
    logger.info(f'Scraping all players whose last name starts with {char} ...')
    link_players_alphabet = main_link + 'players/' + char
    link_lists.append(link_players_alphabet)

list_urls = [link_lists[x:x + 10] for x in range(0, len(link_lists), 10)]
for list in list_urls:
    rs = [grequests.get(u) for u in list]
    results = grequests.map(rs)

    for link in results:
        soup = BeautifulSoup(link.content, 'lxml')
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
            player_name = player_page.find('div', attrs={'itemtype': 'https://schema.org/Person'}).find('h1').text[1:-1]
            # print('player name:', player_name)
            try:
                assert('draft' in str([player_page.find('div', attrs={'itemtype': 'https://schema.org/Person'})
                                      .find_all('p')[8]]))
                data_year_draft = player_page.find('div', attrs={'itemtype': 'https://schema.org/Person'}).find_all('p')[8]
                year_draft = data_year_draft.find_all('a')[1].text[:4]
            except:
                year_draft = 0
            # print('year_draft:', year_draft)
            player_stats = player_page.find('div', attrs={'class': 'stats_pullout'})
            player_stats_p1 = player_stats.find('div', attrs={'class': 'p1'}).find_all('p')
            try:
                total_games = float(player_stats_p1[1].text)
            except:
                total_games = 0
            try:
                total_points = float(player_stats_p1[3].text)
            except:
                total_points = 0
            try:
                total_rebounds = float(player_stats_p1[5].text)
            except:
                total_rebounds = 0
            try:
                total_assists = float(player_stats_p1[7].text)
            except:
                total_assists = 0

            # Inserting into PLAYERS table
            cur.execute("INSERT INTO players ("
                           "name_player, year_draft, number_of_games_career, total_points_career, "
                           "total_rebounds_career, total_assists_career) "
                           "VALUES (%(name)s, %(year_d)s, %(nb_games)s, %(nb_points)s, %(nb_rebounds)s, %(nb_assists)s)",
                        {'name': player_name,
                            'nb_games': total_games,
                            'year_d': year_draft,
                            'nb_points': total_points,
                            'nb_rebounds': total_rebounds,
                            'nb_assists': total_assists})
            connection.commit()

            cur.execute('select last_insert_id()')
            id_player = cur.fetchone()['last_insert_id()']

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
                    cur.execute('SELECT team_name FROM teams WHERE team_name = %(teams)s', {'teams': name_team})
                    team_exists = cur.fetchone()
                    if team_exists is None:
                        # Inserting into TEAMS table only if team is not already in TEAMS table
                        cur.execute("INSERT INTO teams (team_name) VALUES (%(teams)s)", {'teams': name_team})
                        connection.commit()

                    cur.execute('SELECT id_team FROM teams WHERE team_name = %(teams)s', {'teams': name_team})
                    id_team = cur.fetchone()['id_team']
                    # print('id team is ', id_team)
                    # print('id player is ', id_player)
                    # print('year is ', year)

                    # Inserting into TEAMS_TO_PLAYERS table
                    cur.execute("INSERT INTO teams_to_players (id_team, id_player, year) "
                                "VALUES (%(id_team_fk)s, %(id_player_fk)s, %(year_play)s)",
                                {'id_team_fk': id_team,
                                 'id_player_fk': id_player,
                                 'year_play': year})

                    connection.commit()

                except:
                    pass
            # print(player_name, year_draft)
            try:
                # Inserting into DRAFTS table the values we got from the API
                df_id_player = pd.Series(id_player)
                draft_data = tuple(df_id_player.append(get_info_draft_api(player_name, int(year_draft))))
                draft_data = tuple(get_info_draft_api(player_name, int(year_draft)))
                draft_data = get_info_draft_api(player_name, int(year_draft))
                cur.execute("INSERT INTO drafts_api ("
                            "id_player,"
                            "PLAYER_NAME,"
                            "POSITION,"
                            "HEIGHT_WO_SHOES,"
                            "WEIGHT,"
                            "WINGSPAN) "
                            "VALUES (%s, %s, %s, %s, %s, %s)", draft_data)
                connection.commit()
            except:
                pass


    # ----------------------------------------------------------------------------


            # print(draft_data[0], 'for type', type(draft_data.iloc[0]))
            # print(draft_data[1], 'for type', type(draft_data.iloc[1]))
            # print(draft_data[2], 'for type', type(draft_data.iloc[2]))
            # print(draft_data[3], 'for type', type(draft_data.iloc[3]))
            # print(draft_data[4], 'for type', type(draft_data.iloc[4]))
            # cur.execute("INSERT INTO teams_to_players ("
            #             "id_player,"
            #             "PLAYER_NAME,"
            #             "POSITION,"
            #             "HEIGHT_WO_SHOES,"
            #             "WEIGHT,"
            #             "WINGSPAN) "
            #             "VALUES "
            #             "(%(id_play)s, %(name)s, %(pos)s, %(height)s, %(weight)s, %()wingspans)",
            #             {'id_play': id_player,
            #              'name': draft_data.iloc[0],
            #              'pos': draft_data.iloc[1],
            #              'height': draft_data.iloc[2],
            #              'weight': draft_data.iloc[3],
            #              'wingspan': draft_data.iloc[4]})

 # cur.execute("INSERT IGNORE INTO players ( " + cols + ") VALUES (" + "%s," * (len(row) - 1) + "%s)", tuple(row))

# NUMBER_SCRAPED_COLUMNS = 7

# Turning the list into list of lists
# updated_player_list = [player_list[x:x + NUMBER_SCRAPED_COLUMNS]
#                        for x in range(0, len(player_list), NUMBER_SCRAPED_COLUMNS)]
#
# # Storing the data in dataframe and exporting it to database
# player_df = pd.DataFrame(updated_player_list, columns=['name_player',
#                                                        'number_of_games_career',
#                                                        'total_points_career',
#                                                        'total_rebounds_career',
#                                                        'total_assists_career'
#                                                        ])

#  Filling tables line by line
# cur = connection.cur()
#
# cols = ", ".join([str(i) for i in player_df.columns.tolist()])
# print('cols are ', cols)
# for i, row in player_df.iterrows():
#     cur.execute("INSERT IGNORE INTO players ( " + cols + ") VALUES (" + "%s," * (len(row) - 1) + "%s)", tuple(row))


# Deleting duplicates
# cur.execute("DROP TABLE IF EXISTS players_no_duplicates")
# cur.execute("CREATE TABLE players_no_duplicates SELECT DISTINCT name_player,"
#                "number_of_games_career,"
#                "total_points_career,"
#                "total_rebounds_career,"
#                "total_assists_career "
#                "FROM players")
# cur.execute("DROP TABLE players")
# cur.execute("ALTER TABLE players_no_duplicates RENAME TO players")
#
# connection.commit()

# engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
#                        .format(user="root",
#                                pw="pwdmysql",
#                                db="basketball"))
# player_df.to_sql('players', con=engine, if_exists='append', chunksize=1000, index=False)

