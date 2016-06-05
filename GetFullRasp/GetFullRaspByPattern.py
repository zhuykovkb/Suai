# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


class Schedule:
    def __init__(self, time=None, pair=None):
        if time is None:
            self.time = ''
        if pair is None:
            self.pair = []


class Day:
    def __init__(self, day=None, schedule=None):
        if day is None:
            self.day = ''
        if schedule is None:
            self.schedule = []


def GetPattern(pattern, num):
    r = requests.get('http://rasp.guap.ru/?{0}={1}'.format(pattern, num))
    soup = BeautifulSoup(r.content, "html.parser")
    raspData = soup.find('div', {'class': 'result'})

    days = []
    for i in raspData:
        # День недели
        if i.name == 'h3':
            days.append(Day())
            days[-1].day = i.text

        # Время
        elif i.name == 'h4':
            days[-1].schedule.append(Schedule())
            days[-1].schedule[-1].time = '>> {0}'.format(i.text)

        # Пары
        else:
            for span in i.find_all('span'):
                if span.get('class'):
                    continue
                days[-1].schedule[-1].pair.append(span.text.replace('Преподаватель: ', ''))
    return days
