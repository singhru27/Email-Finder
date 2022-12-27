from pymongo import MongoClient
import config

PASSWORD = config.MONGO_PASS

class MongoDao():

    def __init__(self):
        self.client = self.getDatabase(self.getDatabase())
        self.collection = self.getCollection(self.getCollection())
        pass

    def getDatabase(self):
        client = MongoClient("mongodb+srv://singhru:"+config.MONGO_PASS+"@emailservice.bodim.mongodb.net/?retryWrites=true&w=majority")
        return client

    def getCollection(self, collectionName):
        collection = self.client[collectionName]
        return collection

    def insertOne(self, domain, formatID):
        item = {
            "domain" : domain,
            "formatID": formatID
        }
        self.collection.insert_one(item)

    