from bs4 import BeautifulSoup as bs
import requests


def text_pars(self):
    txt = ''
    for i in self:
        txt += i.text
    return txt


def getDollar():
    url_dollar = 'https://quote.rbc.ru/ticker/59111'
    res_d = requests.get(url_dollar)
    soup_d = bs(res_d.text, 'html.parser')
    dollar = soup_d.find_all('span', class_='chart__info__sum')
    return text_pars(dollar)


def getEuro():
    url_euro = 'https://quote.ru/ticker/59090'
    res_e = requests.get(url_euro)
    soup_e = bs(res_e.text, 'html.parser')
    euro = soup_e.find_all('div', class_="MuiGrid-root MuiGrid-item quote-style-1jaw3oe")
    return text_pars(euro)


def getWeather(self):
    url_weather = 'https://weather.rambler.ru/v-moskve/'
    url_wind = 'https://weather.rambler.ru/v-moskve/today/'
    res_w = requests.get(url_weather)
    res_wind = requests.get(url_wind)
    soup_w = bs(res_w.text, 'html.parser')
    soup_wind = bs(res_wind.text, 'html.parser')
    match self:
        case 'gradus':
            weather_gradus = soup_w.find('div', class_='HhSR MBvM')
            return text_pars(weather_gradus)
        case 'wind':
            wind = soup_wind.find('div', class_="hjtR wind HbwD NCAm")
            return text_pars(wind)
        case 'text':
            weathertext = soup_w.find('div', class_='TWnE')
            return text_pars(weathertext)
        case 'intgradus':                                                   #для моей идеи про погоду и одежду
            weather_gradus = soup_w.find('div', class_='HhSR MBvM')
            return int(text_pars(weather_gradus)[:-1])
        case 'intwind':
            wind = soup_wind.find_all('div', class_="hjtR wind HbwD NCAm")
            return int(text_pars(wind)[-5])
print(getWeather('intwind'))

