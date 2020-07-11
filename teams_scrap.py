import sys
import argparse
import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

requete = requests.get('https://www.basketball-reference.com/teams/LAL/2020.html')
page = requete.content
soup = BeautifulSoup(page)
team_player_list = []

team_player_list = []
for year in range(2000, 2020):
    for team in ['CHI', 'TOR', 'LAK', etc]:
        team_year = soup.find('h1').find('span').text[:-3]
        team_player_list.append(team_year)
        team_name = soup.find('h1').find_all('span')
        team_name_final = team_name[1].text
        team_player_list.append(team_name_final)
        team_player = soup.find('tbody').find_all('tr')
        for row in team_player:
              name_player = row.find('td').find('a').text
              team_player_list.append(team_year)
              team_player_list.append(team_name_final)
              team_player_list.append(name_player)

print(team_player_list)
# team_player = soup.find('tbody').find('tr').find('td').find('a').text
# team_player_list.append(team_player)
# print(team_player_list)