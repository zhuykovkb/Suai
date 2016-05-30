from GetFullRasp import GetFullRaspByPattern


# Возвращаем расписание для препода
def Get(teacherId):
    return GetFullRaspByPattern.GetPattern('p', teacherId)