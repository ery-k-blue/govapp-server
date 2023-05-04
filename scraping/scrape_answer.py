import requests
from bs4 import BeautifulSoup

url = 'https://www.shugiin.go.jp/internet/itdb_shitsumon.nsf/html/shitsumon/b211018.htm'

# get info from server
with requests.get(url) as r:
    soup = BeautifulSoup(r.content, 'html.parser')


main_block = soup.find(id = 'mainlayout')
main_divs = main_block.find_all(name='div')
# for i in range(len(main_divs)):
#     print(i)
#     print(main_divs[i])

print(' '.join(main_divs[2].text.split('　')[:-1]))
print(main_divs[2].text.split('　')[-1])


main_element_list = str(main_block).split('<br/>\n')


# for i in range(len(main_element_list)):
#     print(i)
#     print(main_element_list[i])

print(('\n'.join(main_element_list[15:-1])).split('\n<br/>')[0])
