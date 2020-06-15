import requests
from bs4 import BeautifulSoup

# Links (possible de tout réunir dans une liste cf exemple ITC)
link = 'https://www.basketball-reference.com/'

# Assess if connection works
try:
    r = requests.get(link)
except ConnectionError as e:
    print('Connection error')
    raise

# Working with response code
r.status_code == requests.codes.ok
print('request_codes is ', requests.codes['temporary_redirect'])
print('request_codes teapot is ', requests.codes.teapot)
print(requests.codes['o/'])

# Working with headers
resp = requests.head(link)
print('status code is ', resp.status_code,
      ' ; resp_text is ', resp.text,
      ' ; resp_headers are ', resp.headers)
print('encoding is', r.encoding)

# Create pools of proxies and headers and get the first ones (cf exo ITC)
"""
proxies_pool, headers_pool = create_pools()
current_proxy = next(proxy_pool)
current_headers = next(headers_pool)
"""

# START SCRAPING
soup = BeautifulSoup(r.content, 'html.parser')

#print(soup.prettify())
# scores_teams = soup.find_all(class_=["full_table", "team_name"])
# scores_wins = soup.find_all(class_=["full_table", 'data-stat'], id_="wins")
# scores_losses = soup.find_all(class_=["full_table", "team_name"])

# scores = soup.find_all(class_="full_table")
#
#
# # print(scores)
# # print('first elements are ', scores[0])
#
# for tag in scores:
#     # team_name = tag.find(class_='title')
#     # print(team_name)
#     print(tag.text, ' has won ')
#
# row.children[0].text

# Prendre tout le html
gros_tableau = soup.find("div", attrs={'class': "data_grid section_wrapper"})
table_list = gros_tableau.find_all('div', attrs={'class':"table_wrapper"})
print('gros_tableau is ', gros_tableau, '\n')
print('table list is', table_list)
# tableau_2 = gros_tableau.find_all(class_='suppress_all sortable stats_table now_sortable')
# print('tableau2 is ', tableau_2)
# print(len(tableau_2))