import pymongo
conn = pymongo.MongoClient('localhost', 27017)
db = conn.nuaaspider
result = db['nuaa_domin'].find()
for i in result:
    print(i)