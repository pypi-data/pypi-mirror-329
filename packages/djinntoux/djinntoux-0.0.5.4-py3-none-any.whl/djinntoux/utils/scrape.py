from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0'
}

def get_host_and_title(self):
    host_and_title = []
    
    # presumes the consuming model has a field called `link_url`
    host_and_title.append(urlparse(self.link_url).netloc)

    # note that the nytimes.com issue seems to have been eliminated
    '''
    if host_and_title[0] == 'www.nytimes.com':
        host_and_title.append('000 FIX ME PLEASE ***')
        return host_and_title
    else:
    '''
    response = requests.get(self.link_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    host_and_title.append(soup.title.get_text())
    return host_and_title