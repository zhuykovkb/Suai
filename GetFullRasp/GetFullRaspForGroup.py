from GetFullRasp import GetFullRaspByPattern


# Возвращаем расписание для группы
def Get(groupId):
    return GetFullRaspByPattern.GetPattern('g', groupId)
