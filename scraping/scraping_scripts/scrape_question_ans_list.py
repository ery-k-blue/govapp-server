import requests
import json
import os
from bs4 import BeautifulSoup
ELECTION_HTML_URL = 'https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/shiryo/senkyolist.htm'
QUESTION_LIST_URL = 'https://www.shugiin.go.jp/internet/itdb_shitsumon.nsf/html/shitsumon/menu_m.htm'
QUESTION_HTML_URL = 'https://www.shugiin.go.jp/internet/itdb_shitsumon.nsf/html/shitsumon/'
SAVE_DIR = 'scraped_json/'
os.makedirs(SAVE_DIR, exist_ok=True)
SAVE_FILE = 'scraped_questions.json'

ELECTION_HTML_URL = 'https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/shiryo/senkyolist.htm'
with requests.get(ELECTION_HTML_URL) as r:
    election_list_html = BeautifulSoup(r.content, 'html.parser')
election_list_main = election_list_html.find(name='div', attrs={'id':'MainContentsArea2'})
election_list_table = election_list_main.find(name='table')
election_list_last_tr = election_list_table.find_all(name='tr')[-1]
election_list_start_diet = election_list_last_tr.find_all(name='td')[4].text
start_diet_number = int(election_list_start_diet.split('回')[0].replace('第',''))

with requests.get(QUESTION_LIST_URL) as r:
    question_list_html = BeautifulSoup(r.content, 'html.parser')

question_list_select = question_list_html.find(name='select', attrs={'name':'kaiji'})
question_list_option_list = question_list_select.text.split('\n')[1:-2]
diet_number_list = [int(text.split('（')[0].replace('第','').replace('回国会','')) for text in question_list_option_list]
diet_type_list = [text.split('（')[1].replace('）','') for text in question_list_option_list]
diet_list = []
for i in range(len(diet_type_list)):
    diet = dict()
    diet['number'] = diet_number_list[i]
    diet['type'] = diet_type_list[i]
    diet_list.append(diet)
output_data = {'data':diet_list}
with open(SAVE_DIR+'scraped_diets.json', mode='w', encoding='utf-8') as f:
    f.write(json.dumps(output_data, ensure_ascii=False, indent=2))


for diet in diet_list:
    question_list_url = QUESTION_HTML_URL + 'kaiji{}_l.htm'.format(diet['number'])
    with requests.get(question_list_url) as r:
        question_list_html = BeautifulSoup(r.content, 'html.parser')
    question_list_table = question_list_html.find(id = 'shitsumontable')
    question_list_trs = question_list_table.find_all(name = 'tr')
    question_list = []
    for question_list_tr in question_list_trs[1:]:
        question = dict()
        # try getting number
        question['question_number'] = int(question_list_tr.find(attrs={'headers':'SHITSUMON.NUMBER'}).text)
        # try getting title
        td = question_list_tr.find(attrs={'headers':'SHITSUMON.KENMEI'})
        question['title'] = '' if td == None else td.text
        # try getting status
        td = question_list_tr.find(attrs={'headers':'SHITSUMON.STATUS'})
        question['status'] = '' if td == None else td.text
        # try getting progress url
        a = question_list_tr.find(attrs={'headers':'SHITSUMON.KLINK'}).find(name='a')
        question['progress_url'] = '' if a == None else QUESTION_HTML_URL + a.get('href')
        # try getting question url
        a = question_list_tr.find(attrs={'headers':'SHITSUMON.SLINK'}).find(name='a')
        question['question_url'] = '' if a == None else QUESTION_HTML_URL + a.get('href')
        # try getting answer url
        a = question_list_tr.find(attrs={'headers':'SHITSUMON.TLINK'}).find(name='a')
        question['answer_url'] = '' if a == None else QUESTION_HTML_URL + a.get('href')
        # try getting submitter, submitter_party, submit date, transfer date, answer postpone date and answer date from progress_url
        if question['progress_url'] == '':
            question['diet_number'] = ''
            question['submitter_name'] = ''
            question['submitter_party'] = ''
            question['submit_date'] = ''
            question['transfer_date'] = ''
            question['answer_postpone_date'] = ''
            question['answer_date'] = ''
        else:
            with requests.get(question['progress_url']) as r:
                progress_html = BeautifulSoup(r.content, 'html.parser')
            progress_table = progress_html.find(name='table')
            progress_trs = progress_table.find_all(name='tr')
            question['diet_number'] = int(progress_trs[1].find(attrs={'headers':'NAIYO'}).text)
            question['submitter_name'] = progress_trs[5].find(attrs={'headers':'NAIYO'}).text.replace('君','').replace('　','')
            question['submitter_party'] = progress_trs[6].find(attrs={'headers':'NAIYO'}).text
            question['submit_date'] = progress_trs[7].find(attrs={'headers':'NAIYO'}).text
            question['transfer_date'] = progress_trs[8].find(attrs={'headers':'NAIYO'}).text
            question['answer_postpone_date'] = progress_trs[9].find(attrs={'headers':'NAIYO'}).text
            question['answer_date'] = progress_trs[11].find(attrs={'headers':'NAIYO'}).text
        # try getting diet_number and text from question url
        if question['question_url'] == '':
            question['question_text'] = ''
        else:
            with requests.get(question['question_url']) as r:
                question_html = BeautifulSoup(r.content, 'html.parser')
            question_main = question_html.find(id='mainlayout')
            question_element_list = str(question_main).split('<br/>\n')
            question['text'] = '\n'.join(question_element_list[11:-3])
        # try getting respondent position, respondent name and answer text from answer url
        if question['answer_url'] == '':
            question['respondent_position'] = ''
            question['respondent_name'] = ''
            question['answer_text'] = ''
        else:
            with requests.get(question['answer_url']) as r:
                answer_html = BeautifulSoup(r.content, 'html.parser')
            answer_main = answer_html.find(id='mainlayout')
            answer_divs = answer_main.find_all(name='div')
            question['respondent_position'] = ' '.join(answer_divs[2].text.split('　')[:-1])
            question['respondent_name'] = answer_divs[2].text.replace('　','')
            answer_element_list = str(answer_main).split('<br/>\n')
            question['answer_text'] = ('\n'.join(answer_element_list[15:-1])).replace('\n<br/>','')
        question_list.append(question)
        print(question['title'])

    output_data = {'data':question_list}
    with open(SAVE_DIR+str(diet['number'])+'_'+SAVE_FILE, mode='w', encoding='utf-8') as f:
        f.write(json.dumps(output_data, ensure_ascii=False, indent=2))
    
    if diet['number'] == start_diet_number: break

