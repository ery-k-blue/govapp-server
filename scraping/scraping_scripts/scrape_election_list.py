import requests
import json
import os
from bs4 import BeautifulSoup

ELECTION_HTML_URL = 'https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/shiryo/senkyolist.htm'
with requests.get(ELECTION_HTML_URL) as r:
    election_list_html = BeautifulSoup(r.content, 'html.parser')
election_list_main = election_list_html.find(name='div', attrs={'id':'MainContentsArea2'})
election_list_table = election_list_main.find(name='table')
election_list_last_tr = election_list_table.find_all(name='tr')[-1]
election_list_start_diet = election_list_last_tr.find_all(name='td')[4].text
start_diet_number = int(election_list_start_diet.split('回')[0].replace('第',''))
print(start_diet_number)