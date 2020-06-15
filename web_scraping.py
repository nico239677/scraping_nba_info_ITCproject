import requests
from bs4 import BeautifulSoup

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
for row in all_rows:
    print(row.a['title'], ' : ', row.td.nextSibling.nextSibling.text, ' wins, ',
          row.td.nextSibling.nextSibling.nextSibling.text, 'losses')
    #print()
# for row in all_rows.child:
#     print(row)
