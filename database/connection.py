from pymongo import MongoClient

MONGO_URI = "mongodb+srv://ritiksinghis20:hashpassword1199@cluster0.dydw4.mongodb.net"
client = MongoClient(MONGO_URI)
db = client["database1"]
collection = db["users"]

itemcollection=db["items"]