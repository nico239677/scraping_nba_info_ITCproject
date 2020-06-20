import requests
from bs4 import BeautifulSoup
import pandas as pd

# Links
def read_link(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'lxml')
    return soup

main_link = 'https://www.basketball-reference.com/'

# Get global stats
print("\nRESULTS OF THE YEAR SO FAR")

main = read_link(main_link)
score_file = main.find("div", attrs={'class': "data_grid section_wrapper"})
table_list = score_file.find_all('div', attrs={'class': "table_wrapper"})

for table in table_list:
    all_rows = table.find_all("tr", attrs={'class': 'full_table'})
    break
scores = []
for row in all_rows:
    print(row.a['title'] if row.a['title'] else "N/A", ' : ',
          row.td.nextSibling.nextSibling.text if row.td.nextSibling.nextSibling.text else "N/A", ' wins, ',
          row.td.nextSibling.nextSibling.nextSibling.text if row.td.nextSibling.nextSibling.nextSibling.text else "N/A", 'losses')

# Adding data to file, and making sure it exists
    info = [row.a['title'] if row.a['title'] else "N/A",
            row.td.nextSibling.nextSibling.text if row.td.nextSibling.nextSibling.text else "N/A",
            row.td.nextSibling.nextSibling.nextSibling.text if row.td.nextSibling.nextSibling.nextSibling.text else "N/A"]
    scores.append(info)
scores_df = pd.DataFrame(scores, columns=['team', 'wins', 'losses'])
scores_df.to_csv('scores.csv')


print('\n\n LAST SCORES\n')
scores = main.find('div', attrs={'class': 'game_summaries'})
games = scores.find_all('table', attrs={'class': 'teams'})
last_games = []
for game in games:
    loser = game.find('tr', attrs={'class': 'loser'}).find('a').text
    score_loser = game.find('tr', attrs={'class': 'loser'}).find('td', attrs={'class':'right'}).text
    winner = game.find('tr', attrs={'class': 'winner'}).find('a').text
    score_winner = game.find('tr', attrs={'class': 'winner'}).find('td', attrs={'class': 'right'}).text
    print(winner, ' won to ', loser, ' with a score of ', score_winner, ' to ', score_loser)

# Adding data to a csv file
    info_games = [winner if winner else "N/A",
                  loser if loser else "N/A",
                  score_winner if score_winner else "N/A",
                  score_loser if score_loser else "N/A"]
    last_games.append(info_games)
last_games_df = pd.DataFrame(last_games, columns=['Winner', 'Loser', 'Score winner', 'Score loser'])
last_games_df.to_csv('last_games.csv')


print('\n\nCURRENT TRENDING PLAYERS\n')
news = main.find('div', attrs={'id': 'current'})
trending_players = news.find('div').nextSibling.find_all("a")
for player in trending_players:
    print(player.text)


print('\n\nLAST NEWS - RUMORS\n')
rumors = news.find('div').nextSibling.nextSibling.nextSibling.find_all('li')
for rumor in rumors:
    print(rumor.text, 'available at the link: ', rumor.a['href'])

print('\n\n\n----------\n\n\n')

# Getting the data of all drafts for a specific year
YEAR = 2019

print('LIST OF ALL DRAFTS FOR YEAR ', YEAR)

link_draft = main_link + 'draft/NBA_' + str(YEAR) + '.html'

draft = read_link(link_draft)

draft_table = draft.find(class_="overthrow table_container")
body = draft_table.find("tbody").find_all("td")

draft_list = []
for draft in body:
    if 'play-index' in str(draft.find('a')):
        index = draft.find('a').text if draft.find('a').text else "NaN"
        # print(index, end=" ")
        draft_list.append(index)
    if 'players' in str(draft.find('a')):
        name_player = draft.find('a').text if draft.find('a').text else "NaN"
        # print(name_player, end=" ")
        draft_list.append(name_player)
    if 'data-stat="g"' in str(draft):
        number_games = draft.text if draft.text else 'NaN'
        # print('| number of games: ', number_games, end=" ")
        draft_list.append(number_games)
    if 'data-stat="mp_per_g"' in str(draft):
        minutes_played_per_game = draft.text if draft.text else 'NaN'
        # print('| minutes played per game: ', minutes_played_per_game, end=" ")
        draft_list.append(minutes_played_per_game)
    if 'data-stat="pts_per_g"' in str(draft):
        points_per_game = draft.text if draft.text else 'NaN'
    #     # print('| points per games: ', points_per_game, end=" ")
        draft_list.append(points_per_game)
    if 'data-stat="trb_per_g"' in str(draft):
        rebounds_per_game = draft.text if draft.text else 'NaN'
    #     # print('| rebounds per games: ', rebounds_per_game, end=" ")
        draft_list.append(rebounds_per_game)
    if 'data-stat="ast_per_g"' in str(draft):
        assists_per_game = draft.text if draft.text else 'NaN'
    #     # print('| assists per game: ', assists_per_game)
        draft_list.append(assists_per_game)

updated_draft_list = [draft_list[x:x+7] for x in range(0, len(draft_list), 7)]
name = 'list_draft_' + str(YEAR) + '.csv'
draft_df = pd.DataFrame(updated_draft_list, columns=['number_draft',
                                                     'name',
                                                     'number_of_games',
                                                     'minutes_per_game',
                                                     'points_per_game',
                                                     'rebounds_per_game',
                                                     'assists_per_game'
                                                     ''])
print(draft_df)
draft_df.to_csv(name)
