import requests
from bs4 import BeautifulSoup

DIET_MEMBER_HTML_URL = 'https://www.shugiin.go.jp/internet/itdb_giinprof.nsf/html/profile/'
DIET_MEMBERS_HTML_URL = 'https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/syu/'
diet_members_top_url = 'https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/syu/1giin.htm'

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
        member['kanji_name'] = diet_members_tds[0].text
        member['kanji_name'] = ' '.join(member['kanji_name'].split('　')).split('君')[0]
        if diet_members_tds[0].find(name='a') == None:
            member['profile_url'] = ''
        else:
            member['profile_url'] = DIET_MEMBER_HTML_URL + diet_members_tds[0].find(name='a').get('href')
        member['hiragana_name'] = diet_members_tds[1].text
        member['hiragana_name'] = ' '.join(''.join(member['hiragana_name'].split('\n')).split('　'))
        member['party'] = ''.join(diet_members_tds[2].text.split('\n')[:-1])
        member['constituency'] = ''.join(diet_members_tds[3].text.split('\n')[:-1])
        member['election_won_count'] = diet_members_tds[4].text.split('　')[0].split('\n')[0]
        member_list.append(member)
        print(member)

print(member_list[0].keys())