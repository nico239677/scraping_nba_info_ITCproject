from nba_api.stats.endpoints import playergamelog
gamelog_bron = playergamelog.PlayerGameLog(player_id='2544', season = '2018')
df_bron_games_2018 = gamelog_bron.get_data_frames()
print('1sr is\n', df_bron_games_2018)


from nba_api.stats.library.parameters import SeasonAll

gamelog_bron_all = playergamelog.PlayerGameLog(player_id='2544', season = SeasonAll.all)

df_bron_games_all = gamelog_bron_all.get_data_frames()
print('All games Lebron are \n', df_bron_games_all)

# import requests
#
# resp = requests.get('https://stats.nba.com/stats/teamyearbyyearstats?LeagueID=00&PerMode=Totals&SeasonType=Regular+Season&TeamID=1610612739')
#
# data = resp.json()
# for row in data:
#     print(data)
#
#
# series = data['SeasonSeries']
# series

# parameters2 = {'GameDate': '02/14/2015', 'LeagueID': '00', 'DayOffset': 0}

# parameters_league_leader = {"LeagueID": 00, "PerMode": 'Totals', 'StatCategory': 1, 'Season': '2018-19', 'SeasonType': 'Playoffs', 'Scope':'RS'}
# response = requests.get('https://stats.nba.com/stats/leagueleaders', params=parameters_league_leader)

# parameters_yby = {"LeagueID": 00, "PerMode": 'Totals', 'SeasonType': 'Playoffs', 'TeamId': '1610612765'}
# response = requests.get('https://stats.nba.com/stats/teamyearbyyearstats', params=parameters_yby)
# print(response.status_code)
#
# data = response.json()
# print(type(data))
# for element in data:
#     print(element)
# # for row in response.content:
#     print(row)