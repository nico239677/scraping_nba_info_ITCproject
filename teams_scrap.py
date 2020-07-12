import argparse
from tqdm import tqdm
from datetime import datetime
import pandas as pd
from functions import *

list_teams = ['TOR', 'BOS', 'PHI', 'BRK', 'NYK', 'DEN', 'UTA', 'OKC', 'POR', 'MIN', 'MIL', 'IND', 'CHI', 'DET', 'CLE',
              'LAL', 'LAC', 'SAC', 'PHO', 'GSW', 'MIA', 'ORL', 'WAS', 'CHO', 'ATL', 'HOU', 'DAL', 'MEM', 'NOP', 'SAS']
NUMBER_SCRAPED_COLUMNS = 3

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
parser.add_argument('-teams_to_scrap',
                    '--teams',
                    type=str,
                    nargs='*',
                    default=list_teams,
                    help='choose teams to scrap')
args = parser.parse_args()


main_link = "https://www.basketball-reference.com/teams/"
end_link = '.html'

# Getting the data of all teams' players for a specific period of time
FIRST_YEAR = args.start_year
LAST_YEAR = args.end_year
TEAMS = args.teams

# Checking that LAST_YEAR comes after FIRST_YEAR
try:
    assert (LAST_YEAR >= FIRST_YEAR)
except AssertionError:
    print("Last year to scrap should be higher than first year")
    sys.exit()

# Checking that TEAMS only contains real teams
try:
    assert all(elem in list_teams for elem in TEAMS)
except AssertionError:
    print("Please enter valid team acronyms")
    sys.exit()


team_player_list = []
for team in tqdm(TEAMS):
    print('scraping team', team)
    for year in range(FIRST_YEAR, LAST_YEAR+1):
        total_link = main_link + team + '/' + str(year) + end_link
        team_page = read_link(total_link)
        try:
            team_year = team_page.find('h1').find('span').text[:-3]
            # team_name = team_page.find('h1').find_all('span')
        except AttributeError:
            print('Link not valid: team', team, 'does not have data for year', year)
            continue
        team_year = year
        team_name = team_page.find('h1').find_all('span')[1].text
        team_player = team_page.find('tbody').find_all('tr')
        for row in team_player:
              name_player = row.find('td').find('a').text
              team_player_list.append(team_year)
              team_player_list.append(team_name)
              team_player_list.append(name_player)

# Turning the list into list of lists
updated_teams_list = [team_player_list[x:x + NUMBER_SCRAPED_COLUMNS]
                      for x in range(0, len(team_player_list), NUMBER_SCRAPED_COLUMNS)]

# Storing the data in dataframe and exporting it to database
teams_df = pd.DataFrame(updated_teams_list, columns=['year',
                                                     'team_name',
                                                     'team_player'])

#  Filling tables line by line
cursor = connection.cursor()

cols = ", ".join([str(i) for i in teams_df.columns.tolist()])
for i, row in teams_df.iterrows():
    cursor.execute("INSERT IGNORE INTO teams ( " + cols + ") VALUES (" + "%s,"*(len(row)-1) + "%s)", tuple(row))

# Deleting duplicates
cursor.execute("DROP TABLE IF EXISTS teams_no_duplicates")
cursor.execute("CREATE TABLE teams_no_duplicates SELECT DISTINCT year,"
               "team_name,"
               "team_player "
               "FROM teams")
cursor.execute("DROP TABLE teams")
cursor.execute("ALTER TABLE teams_no_duplicates RENAME TO teams")

connection.commit()