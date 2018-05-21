from pymongo import MongoClient
from config import MONGO_URI,MONGO_DB
from pprint import pprint

try:
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
except Exception as err:
    print(str(err))

def createUser(obj):
    try:
        users = db['users']
        u = users.insert(obj)
        return {"success" : True}
    except  Exception as e:
        return {"success" : False , "error":e}

def checkUser(obj):
    try:
        users = db['users']
        u = users.find_one(obj)
        if(u):
            return {"success" : True, "exists" : True, "user" : u}
        else:
            return {"success" : True, "exists" : False}
    except  Exception as e:
        return {"success" : False,"error":e}

def addDocument(obj):
    try:
        docs = db['docs']
        d = docs.insert(obj)
        return {"success" : True}
    except  Exception as e:
        return {"success" : False , "error":e}


def getDocuments(obj):
    try:
        docs = db['docs']
        return docs.find(obj)
    except  Exception as e:
        return {"success": False, "error": e}

def delDocument(obj):
    try:
        docs = db['docs']
        d = docs.delete_one(obj)
        return {"success" : True}
    except  Exception as e:
        return {"success": False, "error": e}
