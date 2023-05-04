import requests
from bs4 import BeautifulSoup

url = 'https://www.shugiin.go.jp/internet/itdb_shitsumon.nsf/html/shitsumon/a211002.htm'

# get info from server
with requests.get(url) as r:
    soup = BeautifulSoup(r.content, 'html.parser')


main_block = soup.find(id = 'mainlayout')
main_element_list = str(main_block).split('<br/>\n')

print('\n'.join(main_element_list[11:-3]))
