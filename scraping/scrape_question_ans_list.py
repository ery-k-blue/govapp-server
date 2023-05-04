import requests
from bs4 import BeautifulSoup

QUESTION_LIST_URL = 'https://www.shugiin.go.jp/internet/itdb_shitsumon.nsf/html/shitsumon/menu_m.htm'
QUESTION_HTML_URL = 'https://www.shugiin.go.jp/internet/itdb_shitsumon.nsf/html/shitsumon/'
with requests.get(QUESTION_LIST_URL) as r:
    question_list_html = BeautifulSoup(r.content, 'html.parser')

question_list_table = question_list_html.find(id = 'shitsumontable')
question_list_trs = question_list_table.find_all(name = 'tr')
question_list = []
for question_list_tr in question_list_trs[1:]:
    question = dict()
    # try getting number
    td = question_list_tr.find(attrs={'headers':'SHITSUMON.NUMBER'})
    question['question_number'] = '' if td == None else td.text
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
        question['diet_number'] = progress_trs[1].find(attrs={'headers':'NAIYO'}).text
        question['submitter_name'] = ' '.join(progress_trs[5].find(attrs={'headers':'NAIYO'}).text.split('君')[0].split('　'))
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
        question['respondent_name'] = answer_divs[2].text.split('　')[-1]
        answer_element_list = str(answer_main).split('<br/>\n')
        question['answer_text'] = ('\n'.join(answer_element_list[15:-1])).split('\n<br/>')[0]
    question_list.append(question)
    print(question['title'])

print(len(question_list))