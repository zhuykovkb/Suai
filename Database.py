from pymongo import MongoClient

client = MongoClient()
db = client['SUAI']
collection = db['students']

"""

# find all documents
results = collection.find()

for record in results:
    print(str(record['ID']) + ',', record['Name'] + ',', record['Group'])

"""


# collection.delete_one({'ID':873863})

def InsertStudent(id, name, group):
    student = {"id": id, "name": name, "group": group}

    collection.insert(student)


def GetStudent(id):
    return collection.find_one({'id': id})


def DeleteAllRecords():
    db.drop_collection('students')


def DeleteById(id):
    collection.delete_one({'id': id})