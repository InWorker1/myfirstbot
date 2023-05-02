from bs4 import BeautifulSoup as bs
import requests

curs_dollar = ''
curs_euro = ''

url_dollar = 'https://quote.rbc.ru/ticker/59111'
res_d = requests.get(url_dollar)
soup_d = bs(res_d.text,  'html.parser')

dollar = soup_d.find_all('span', class_='chart__info__sum')
for i in dollar:
    curs_dollar += '' if i == ' ' else i.text

url_euro = 'https://quote.ru/ticker/59090'
res_e = requests.get(url_euro)
soup_e = bs(res_e.text, 'html.parser')

euro = soup_e.find_all('div', class_="MuiGrid-root MuiGrid-item quote-style-1jaw3oe")
for i in euro:
    curs_euro += '' if i == ' ' else i.text

print(curs_euro)
print(curs_dollar)
