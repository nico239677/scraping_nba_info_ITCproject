import requests
from bs4 import BeautifulSoup

# Links (possible de tout réunir dans une liste cf exemple ITC)
link = 'https://www.basketball-reference.com/'
link_results = 'https://www.basketball-reference.com/boxscores/'

# Assess if connection works
try:
    r1 = requests.get(link)
except ConnectionError as e:
    print('Connection error')
    raise

# Working with response code
r1.status_code == requests.codes.ok
print(requests.codes['temporary_redirect'])
print(requests.codes.teapot)
print(requests.codes['o/'])

# Working with headers
resp = requests.head(link)
print(resp.status_code, resp.text, resp.headers)
print(r.encoding)

# Create pools of proxies and headers and get the first ones (cf exo ITC)
proxies_pool, headers_pool = create_pools()
current_proxy = next(proxy_pool)
current_headers = next(headers_pool)

# START SCRAPING
soup1 = BeautifulSoup(r1.content, 'html.parser')
soup2 = BeautifulSoup(r2.content, 'html.parser')
#print(soup.prettify())
scores = soup1.find(class_="game_summary expanded nohover")
scores = soup2.find(class_="table_wrapper")
