import requests
import datetime
import GetFullRaspForGroup
import Constaints
from bs4 import BeautifulSoup

addressPattern = 'http://rasp.guap.ru/?{0}={1}'

r = requests.get("http://rasp.guap.ru/")
soup = BeautifulSoup(r.content)

pairty = ''

db = []

groups = {}
teachers = {}
build = {}
rooms = {}

db.append(groups)
db.append(teachers)
db.append(build)
db.append(rooms)

i = 0
for row in soup.find_all('select'):
    for opt in row.find_all('option'):
        db[i][opt.text.upper()] = opt.get('value')
    i += 1


# Получить ID группы
def GetGroupID(group):
    for gItem in db[0]:
        if gItem.find(group.upper()) >= 0:
            try:
                return db[0][gItem]
            except:
                return '-1'
    return '-2'


# Получить ID препода
def GetTeacherID(teacher):
    if teacher == '':
        return 'Запрос пуст\nФормат запроса: /tch фамилия'

    for tItem in db[1]:
        if tItem.find(teacher.upper()) >= 0:
            try:
                return addressPattern.format('Препод', tItem, 'p', db[1][tItem])
            except:
                return 'Error: {0}; sName: {1}'.format('GetTeacherID', tItem)

    return 'Неудается найти "{0}" :('.format(teacher.upper())


# Получить четность недели
def GetPairty():
    pairty = soup.find('em').text
    return pairty


# Получить расписание на неделю
def GetWeekRasp(groupName):
    if groupName == '':
        return 'Запрос пуст\nФормат запроса: /group 0000'

    groupId = GetGroupID(groupName)
    if groupId == '-1':
        return 'Ошибка -1'
    elif groupId == '-2':
        return 'Ошибка -2'

    days = GetFullRaspForGroup.Get(groupId)
    result = []

    for day in days:
        result.append('••••••••••')
        result.append(day.day)
        result.append('••••••••••')
        for shedule in day.shdl:
            result.append(shedule.time)
            for pair in shedule.pair:
                if pair != shedule.pair[-1]:
                    result.append(pair)
                else:
                    result.append('{0}\n'.format(pair))

    return '\n'.join(result)


# Получить расписание на сегодня
def GetTodayRasp(groupName):
    if groupName == '':
        return 'Запрос пуст\nФормат запроса: /group 0000'

    groupId = GetGroupID(groupName)
    if groupId == '-1':
        return 'Ошибка -1'
    elif groupId == '-2':
        return 'Ошибка -2'

    days = GetFullRaspForGroup.Get(groupId)
    result = []

    wkind = datetime.date.today().weekday()
    currentDay = Constaints.Weeks[wkind]

    for day in days:
        if day.day.upper() == currentDay.upper():
            result.append('••••••••••')
            result.append(day.day)
            result.append('••••••••••')
            for shedule in day.shdl:
                result.append(shedule.time)
                for pair in shedule.pair:
                    if pair != shedule.pair[-1]:
                        result.append(pair)
                    else:
                        result.append('{0}\n'.format(pair))
            break

    if len(result) == 0:
        result.append('\n{0}\n'.format('Расписания нет'))

    return '\n'.join(result)


# Получить расписание на завтра
def GetTomorrowRasp(groupName):
    if groupName == '':
        return 'Запрос пуст\nФормат запроса: /group 0000'

    groupId = GetGroupID(groupName)
    if groupId == '-1':
        return 'Ошибка -1'
    elif groupId == '-2':
        return 'Ошибка -2'

    days = GetFullRaspForGroup.Get(groupId)
    result = []

    wkind = datetime.date.today().weekday() + 1;
    if wkind > 5:
        wkind = 0

    currentDay = Constaints.Weeks[wkind]

    for day in days:
        if day.day.upper() == currentDay.upper():
            result.append('••••••••••')
            result.append(day.day)
            result.append('••••••••••')
            for shedule in day.shdl:
                result.append(shedule.time)
                for pair in shedule.pair:
                    if pair != shedule.pair[-1]:
                        result.append(pair)
                    else:
                        result.append('{0}\n'.format(pair))
            break

    if len(result) == 0:
        result.append('\nНа {0} {1}\n'.format(datetime.date.today(), 'Расписания нет'))

    return '\n'.join(result)
