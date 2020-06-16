import requests
from bs4 import BeautifulSoup
import pandas as pd

# Links (possible de tout réunir dans une liste cf exemple ITC)
link = 'https://www.basketball-reference.com/'
r = requests.get(link)

soup = BeautifulSoup(r.content, 'lxml')

# Get global stats
print("RESULTS OF THE YEAR SO FAR")
gros_tableau = soup.find("div", attrs={'class': "data_grid section_wrapper"})
table_list = gros_tableau.find_all('div', attrs={'class':"table_wrapper"})

for table in table_list:
    all_rows = table.find_all("tr", attrs={'class':'full_table'})
    break
scores = []
for row in all_rows:
    # print(row.a['title'], ' : ', row.td.nextSibling.nextSibling.text, ' wins, ',
    #       row.td.nextSibling.nextSibling.nextSibling.text, 'losses'))
    info = [row.a['title'], row.td.nextSibling.nextSibling.text, row.td.nextSibling.nextSibling.nextSibling.text]
    scores.append(info)
scores_df = pd.DataFrame(scores, columns=['team', 'wins', 'losses'])
print('scores df is ', scores_df)
scores_df.to_csv('scores.csv')

print('\n\n LAST SCORES\n')
scores = soup.find('div', attrs={'class': 'game_summaries'})
games = scores.find_all('table', attrs={'class': 'teams'})
for game in games:
    loser = game.find('tr', attrs={'class': 'loser'}).find('a').text
    winner = game.find('tr', attrs={'class': 'winner'}).find('a').text
    print(winner, ' won to ', loser)

print('\n\nCURRENT TRENDING PLAYERS\n')
news = soup.find('div', attrs={'id': 'current'})
#print(news)
trending_players = news.find('div').nextSibling.find_all("a")
for player in trending_players:
    print(player.text)

print('\n\nLAST NEWS - RUMORS\n')
rumors = news.find('div').nextSibling.nextSibling.nextSibling.find_all('li')
for rumor in rumors:
    print(rumor.text, 'available at the link: ', rumor.a['href'])


# Add content to text file
# with open('scraping_projet.txt', 'wt') as file:
#     file.write(content)
# f = csv.writer(open('results.csv', 'w'))
# f.writerow([])