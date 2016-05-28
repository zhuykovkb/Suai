import requests
from bs4 import BeautifulSoup


class Shedule:
    def __init__(self, time=None, pair=None):
        if time is None:
            self.time = ''
        if pair is None:
            self.pair = []


class Day:
    def __init__(self, day=None, shdl=None):
        if day is None:
            self.day = ''
        if shdl is None:
            self.shdl = []


def Get(groupId):
    r = requests.get('http://rasp.guap.ru/?g={0}'.format(groupId))
    soup = BeautifulSoup(r.content)
    raspData = soup.find('div', {'class': 'result'})

    days = []
    for i in raspData:
        # День недели
        if i.name == 'h3':
            days.append(Day())
            days[-1].day = i.text

        # Время
        elif i.name == 'h4':
            days[-1].shdl.append(Shedule())
            days[-1].shdl[-1].time = '>> {0}'.format(i.text)

        # Пары
        else:
            for span in i.find_all('span'):
                if span.get('class'):
                    continue
                days[-1].shdl[-1].pair.append(span.text.replace('Преподаватель: ', ''))

    return days
