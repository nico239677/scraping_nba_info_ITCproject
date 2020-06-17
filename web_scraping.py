import requests
from bs4 import BeautifulSoup
import pandas as pd

# Links
link = 'https://www.basketball-reference.com/'
r = requests.get(link)
soup = BeautifulSoup(r.content, 'lxml')

# Get global stats
print("\nRESULTS OF THE YEAR SO FAR")

score_file = soup.find("div", attrs={'class': "data_grid section_wrapper"})
table_list = score_file.find_all('div', attrs={'class': "table_wrapper"})

for table in table_list:
    all_rows = table.find_all("tr", attrs={'class': 'full_table'})
    break
scores = []
for row in all_rows:
    print('row is ', row)
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
scores = soup.find('div', attrs={'class': 'game_summaries'})
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
news = soup.find('div', attrs={'id': 'current'})
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

link_draft = 'https://www.basketball-reference.com/draft/NBA_' + str(YEAR) + '.html'
r2 = requests.get(link_draft)

soup = BeautifulSoup(r2.content, 'lxml')
draft_table = soup.find("div", attrs={'class': "table_outer_container"})
body = draft_table.find("tbody")
print(body)
for row in body:
    print(row.find("a").nextSibling)

# for row in body:
#     print(row)
#     name_player = all_rows.find_all('td', attrs={'class': 'left'})
# print('name player is ', name_player)
    #print(row.td.nextSibling.nextSibling.text)
    #tbody.td.nextSibling.nextSibling.a.text)
#print(all_rows)
# for row in all_rows:
#     print(row)
# print(draft_table)
# draft_file_df = pd.DataFrame(draft_table)
# name_file = 'draft_year_' + str(YEAR) + '.csv'
# draft_file_df.to_csv(name_file)
