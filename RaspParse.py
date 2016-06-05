# -*- coding: utf-8 -*-

import datetime

import requests
import Constaints

from bs4 import BeautifulSoup
from GetFullRasp import GetFullRaspForGroup
from GetFullRasp import GetFullRaspForTeacher

db = []

def UpdatesAllIDs():
    r = requests.get("http://rasp.guap.ru/")
    soup = BeautifulSoup(r.content, "html.parser")

    res = []

    groups = {}
    teachers = {}
    build = {}
    rooms = {}

    res.append(groups)
    res.append(teachers)
    res.append(build)
    res.append(rooms)

    i = 0
    for row in soup.find_all('select'):
        for opt in row.find_all('option'):
            res[i][opt.text.upper()] = opt.get('value')
        i += 1

    return res


# Получить ID группы
def GetGroupID(group):
    db = UpdatesAllIDs()

    for gItem in db[0]:
        if gItem.find(group.upper()) >= 0:
            try:
                return db[0][gItem]
            except:
                return '-1'
    return '-2'


# Получить ID препода
def GetTeacherRasp(teacher):
    db = UpdatesAllIDs()

    if teacher == '':
        return 'Запрос пуст\nФормат запроса: /tch фамилия'

    # Ищем препода по фамиилии
    for tItem in db[1]:
        if tItem.find(teacher.upper()) >= 0:
            days = GetFullRaspForTeacher.Get(db[1].get(tItem))
            break

    # Ситуация если препода не нашли - выходим
    if not days:
        return 'Неудается найти "{0}" :('.format(teacher.upper())

    # Соответственно вывод инфармации о расписании если препод нашелся
    result = [tItem]
    for day in days:
        result.append('••••••••••')
        result.append(day.day)
        result.append('••••••••••')
        for schedule in day.schedule:
            result.append(schedule.time)
            for pair in schedule.pair:
                if pair != schedule.pair[-1]:
                    result.append(pair)
                else:
                    result.append('{0}\n'.format(pair))

    return '\n'.join(result)


# Получить четность недели
def GetParity():
    r = requests.get("http://rasp.guap.ru/")
    soup = BeautifulSoup(r.content, "html.parser")

    return soup.find('em').text


# Получить расписание на неделю
def GetWeekRasp(groupName):
    if groupName == '':
        return Constaints.WrongRequestAnswer.format('wk')

    groupId = GetGroupID(groupName)
    if groupId == '-1':
        return 'Ошибка -1'
    elif groupId == '-2':
        return 'Ошибка -2'

    days = GetFullRaspForGroup.Get(groupId)
    result = []

    for day in days:
        dots = MakeDotsByLen(day.day)

        result.append(dots)
        result.append(day.day)
        result.append(dots)
        for schedule in day.schedule:
            result.append(schedule.time)
            for pair in schedule.pair:
                if pair != schedule.pair[-1]:
                    result.append(pair)
                else:
                    result.append('{0}\n'.format(pair))

    return '\n'.join(result)


# Получить расписание на сегодня
def GetTodayRasp(groupName):
    if groupName == '':
        return Constaints.WrongRequestAnswer.format('td')

    groupId = GetGroupID(groupName)
    if groupId == '-1':
        return 'Ошибка -1'
    elif groupId == '-2':
        return Constaints.WrongGroup

    days = GetFullRaspForGroup.Get(groupId)
    result = []

    # получаю индекс дня недели
    wkind = datetime.date.today().weekday()

    # устанавливаю текущий день недели
    currentDay = Constaints.Weeks[wkind]

    for day in days:
        if day.day.upper() == currentDay.upper():
            dots = MakeDotsByLen(day.day)

            result.append(dots)
            result.append(day.day)
            result.append(dots)
            for schedule in day.schedule:
                result.append(schedule.time)
                for pair in schedule.pair:
                    if pair != schedule.pair[-1]:
                        result.append(pair)
                    else:
                        result.append('{0}\n'.format(pair))
            break

    if len(result) == 0:
        result.append('\n{0}\n'.format('Выходной'))

    return '\n'.join(result)


# Получить расписание на завтра
def GetTomorrowRasp(groupName):
    if groupName == '':
        return Constaints.WrongRequestAnswer.format('tm')

    groupId = GetGroupID(groupName)
    if groupId == '-1':
        return 'Ошибка -1'
    elif groupId == '-2':
        return 'Ошибка -2'

    days = GetFullRaspForGroup.Get(groupId)
    result = []

    # получаю индекс завтрашнего дня недели
    wkind = datetime.date.today().weekday() + 1

    # проверка на границу недели с тем исключением, что
    # в случае запроса в Субботу, результат вернется не на
    # Воскрсенье, а в Понедельник
    if wkind > 5:
        wkind = 0

    currentDay = Constaints.Weeks[wkind]

    for day in days:
        if day.day.upper() == currentDay.upper():
            dots = MakeDotsByLen(day.day)

            result.append(dots)
            result.append(day.day)
            result.append(dots)
            for schedule in day.schedule:
                result.append(schedule.time)
                for pair in schedule.pair:
                    if pair != schedule.pair[-1]:
                        result.append(pair)
                    else:
                        result.append('{0}\n'.format(pair))
            break

    if len(result) == 0:
        result.append('\nНа {0} {1}\n'.format(datetime.date.today(), 'Выходной'))

    return '\n'.join(result)


# Нужное количество точек
def MakeDotsByLen(text):
    str = ''
    for i in text:
        str += '●'
    return str
