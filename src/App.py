import csv
import config
import json
import sys
sys.path.insert(0, 'Model')
sys.path.insert(0, '..')
import MongoDAO
import progressbar
from validate_email import MailtesterSingle


class EmailWriter():
    def __init__(self):
        self.apiCounter = 0

    def getEmailFormat(self, firstName, lastName, company, domain, role):
        """
        Input: Set of parameters describing a potential email contact
        Output: True if succesfully entered into the database, false if a match was not successfully found
        """

        if not firstName or not lastName or not domain:
            return None

        emailList = []
        emailList.append(firstName + lastName + "@" + domain)
        emailList.append(firstName + "." + lastName + "@" + domain)
        emailList.append(firstName[0] + lastName + "@" + domain)
        emailList.append(firstName[0] + "." + lastName + "@" + domain)
        emailList.append(lastName + firstName + "@" + domain)
        emailList.append(lastName + "." + firstName[0] + "@" + domain)
        emailList.append(firstName + "_" + lastName + "@" + domain)
        emailList.append(firstName[0] + "_" + lastName + "@" + domain)
        emailList.append(firstName + lastName[0] + "@" + domain)
        emailList.append(lastName + "." + firstName + "@" + domain)
        emailList.append(firstName + "@" + domain)
        emailList.append(firstName + "." + lastName[0] + "@" + domain)
        emailList.append(lastName + firstName[0] + "@" + domain)
        emailList.append(lastName[0] + firstName + "@" + domain)
        emailList.append(firstName[0] + "-" + lastName + "@" + domain)
        emailList.append(firstName + "-" + lastName[0] + "@" + domain)
        emailList.append(lastName + "-" + firstName + "@" + domain)
        emailList.append(lastName + "_" + firstName + "@" + domain)
        emailList.append(firstName + "-" + lastName + "@" + domain)

        # Checking for duplicates
        for email in emailList:
            if self.checkForExistence(email):
                return True
            
        
        MongoUserDAO = MongoDAO.MongoUserDAO()
        MongoFormatDAO = MongoDAO.MongoFormatDAO()

        for email in emailList:
            self.apiCounter += 1
            E = MailtesterSingle(config.API_KEY, email)
            res = E.control()
            res = json.loads(res)
            if res["result"] == "valid":
                self.writeToCSV(firstName, lastName, company, domain, role, email)
                MongoUserDAO.insertOne(firstName, lastName, company, domain, role, email, True)    
                return True
            elif res["result"] == "unknown" or res["result"] == "risky":
                self.writeToCSV(firstName, lastName, company, domain, role, email, "x")
                MongoUserDAO.insertOne(firstName, lastName, company, domain, role, email, True)    
                return True

        return False

    def checkForExistence(self, email):
        """
        Input: Prospective email
        Output: Boolean indicating whether this email has already been entered into the database
        """
        MongoUserDAO = MongoDAO.MongoUserDAO()
        res = list(MongoUserDAO.findByEmail({"email": email}))
        if len(res) > 0:
            return True
        return False


    def writeToCSV(self, firstName, lastName, company, domain, role, email, tag=None):

        with open("emails.csv", "a") as destinationFile:
            emailWriter = csv.writer(destinationFile)
            if tag:
                emailWriter.writerow([firstName + " " + lastName, company, domain, role, email, "x"])
            else:
                emailWriter.writerow([firstName + " " + lastName, company, domain, role, email])
        
    def convertCSV(self, fileName):
        with open(fileName) as sourceFile:
            emailReader = csv.reader(sourceFile)
            for i, row in enumerate(emailReader):
                name = row[0].split()
                firstName = name[0]
                lastName = name[1]
                company = row[1]
                domain = row[2]
                role = row[3]
                self.getEmailFormat(firstName, lastName, company, domain, role)
                print(self.apiCounter)
    def loadToMongo(self, filePath):
        counter = 0
        MongWriter = MongoDAO.MongoUserDAO()

        with open(filePath) as sourceFile:
            emailReader = csv.reader(sourceFile)
            rowCount = sum(1 for row in emailReader)
            bar = progressbar.ProgressBar(maxval=rowCount).start()

        with open(filePath) as sourceFile:
            emailReader = csv.reader(sourceFile)
            for i, row in enumerate(emailReader):
                if i == 0:
                    continue
                name = row[0].split()
                firstName = name[0]
                lastName = name[1]
                company = row[1]
                domain = row[2]
                role = row[3]       
                email = row[4]
                unknownStatus = True if row[5] == "x" else False
                MongWriter.insertOne(firstName, lastName, company, domain, role, email, unknownStatus)    
                counter += 1
                bar.update(counter)

if __name__ == "__main__":
    EmailWriter = EmailWriter()
    print("Please select your option \n 1: Load Data to Mongo \n 2: Convert CSV to Emails")
    firstChoice = input()
    if firstChoice == "1":
        print("Please enter the the name of the file you want to load")
        fileName = input()
        EmailWriter.loadToMongo(fileName)
    elif firstChoice == "2":
        print("Please enter the name of the file you want to find emails for")
        fileName = input()
        EmailWriter.convertCSV(fileName)

        
