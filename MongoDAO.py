from pymongo import MongoClient
import config
PASSWORD = config.MONGO_PASS

class MongoDAO():
    def __init__(self):
        self.client = self.getDatabase()

    def getDatabase(self):
        client = MongoClient("mongodb+srv://singhru:"+config.MONGO_PASS+"@emailservice.bodim.mongodb.net/?retryWrites=true&w=majority")
        return client["Emails"]


class MongoFormatDao(MongoDAO):

    def __init__(self):
        super().__init__()
        self.collection = self.getCollection()
        pass

    def getCollection(self):
        collection = self.client["Email_Keys"]
        return collection

    def insertOne(self, domain, formatID):
        item = {
            "domain" : domain,
            "formatID": formatID
        }
        self.collection.insert_one(item)

class MongoUserDAO(MongoDAO):
    def __init__(self):
        super().__init__()
        self.collection = self.getCollection()

    def getCollection(self):
        collection = self.client["User_Database"]
        return collection

    def insertOne(self, firstName, lastName, company, domain, role, email, unknownStatus):
        item = {
            "firstName" : firstName,
            "lastName": lastName,
            "company": company,
            "domain": domain,
            "role": role,
            "email": email,
            "unknownStatus": unknownStatus
        }
        self.collection.insert_one(item)
    