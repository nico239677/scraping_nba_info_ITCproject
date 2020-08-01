import requests
from bs4 import BeautifulSoup
from gevent import monkey as curious_george
curious_george.patch_all(thread=False, select=False)


def read_link(link):
    """Reads link to manipulate it with BeautifulSoup"""
    # Handles error if link is incorrect
    try:
        r = requests.get(link)
        # print('link: \n', link)
    except requests.exceptions.ConnectionError:
        print('URL not valid')
        pass
    soup = BeautifulSoup(r.content, 'lxml')
    return soup


def add_tag_link_and_year(global_list, draft, string, year_draft):
    """Adds the player draft number and draft year"""
    if string in str(draft.find('a')):
        element = draft.find('a').text if draft.find('a').text else None
        global_list.append(year_draft)
        global_list.append(element)
        return


def add_text_in_tag(global_list, draft, string):
    """Adds player stats depending text in tag"""
    if string in str(draft):
        element = draft.text if draft.text else None
        global_list.append(element)
        return


def find_year_draft(player_page):
    """Scraps draft year if exists"""
    i = 5
    while i < 10:
        if 'draft' in str([player_page.find('div', attrs={'itemtype': 'https://schema.org/Person'})
                               .find_all('p')[i]]):
            data_year_draft = player_page.find('div', attrs={'itemtype': 'https://schema.org/Person'}).find_all('p')[i]
            year = data_year_draft.find_all('a')[1].text[:4]
            return year
        i += 1

