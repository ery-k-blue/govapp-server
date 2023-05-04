import requests
import json
import os
from bs4 import BeautifulSoup

DIET_MEMBER_HTML_URL = 'https://www.shugiin.go.jp/internet/itdb_giinprof.nsf/html/profile/'
DIET_MEMBERS_HTML_URL = 'https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/syu/'
diet_members_top_url = 'https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/syu/1giin.htm'
SAVE_DIR = 'scraped_json/'
os.makedirs(SAVE_DIR, exist_ok=True)
SAVE_FILE = 'scraped_members.json'
# get all page url
diet_members_url_list = []
with requests.get(diet_members_top_url) as r:
    diet_members_html = BeautifulSoup(r.content, 'html.parser')
diet_members_mainlayout = diet_members_html.find(id='mainlayout')

diet_members_as = diet_members_mainlayout.find_all(name='p')[0].find_all(name='a')
for diet_members_a in diet_members_as:
    diet_members_url_list.append(DIET_MEMBERS_HTML_URL+diet_members_a.get('href'))

# get all members data
member_list = []
for diet_members_url in diet_members_url_list:
    with requests.get(diet_members_url) as r:
        diet_members_html = BeautifulSoup(r.content, 'html.parser')
    diet_members_mainlayout = diet_members_html.find(id='mainlayout')
    diet_members_sh1body = diet_members_mainlayout.find(id='sh1body')
    diet_members_trs = diet_members_sh1body.find_all(name='tr')[3:-1]
    for diet_members_tr in diet_members_trs:
        diet_members_tds = diet_members_tr.find_all(name='td')
        member = dict()
        member['kanji_name'] = diet_members_tds[0].text.replace('　','').replace('\n','').replace('君','')
        if diet_members_tds[0].find(name='a') == None:
            member['profile_url'] = ''
        else:
            member['profile_url'] = DIET_MEMBER_HTML_URL + diet_members_tds[0].find(name='a').get('href')
        member['hiragana_name'] = diet_members_tds[1].text.replace('\n','').replace('　','')
        member['party'] = diet_members_tds[2].text.replace('\n','')
        member['constituency'] = diet_members_tds[3].text.replace('\n','').replace('　','')
        member['election_won_count'] = diet_members_tds[4].text.replace('　','').replace('\n', '').replace(' ', '')
        member_list.append(member)
        print(member)
output_data = {'data':member_list}
with open(SAVE_DIR+SAVE_FILE, mode='w', encoding='utf-8') as f:
    f.write(json.dumps(output_data, ensure_ascii=False, indent=2))

print(member_list[0].keys())