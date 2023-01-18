import csv
import config
import json
import sys
sys.path.insert(0, 'Model')
sys.path.insert(0, 'Data')
sys.path.insert(0, '..')
sys.path.insert(0, "Controller")
import MongoDAO
import progressbar
import requests
import time
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
        emailList.append(firstName + lastName + "@" + domain)
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

        # # Check for domain
        # currFormat = self.checkForFormat(domain)
        # if currFormat:
        #     email = emailList[currFormat["formatID"]]
        #     E = MailtesterSingle(config.API_KEY, email)
        #     res = E.control()
        #     res = json.loads(res)
        #     print(res)
        #     if res["result"] == "valid" or res["result"] == "unknown" or res["result"] == "risky":
        #         self.writeToCSV(firstName, lastName, company, domain, role, email)
        #         return True                
            
        MongoUserDAO = MongoDAO.MongoUserDAO()
        MongoFormatDAO = MongoDAO.MongoFormatDAO()

        for i, email in enumerate(emailList):
            self.apiCounter += 1

            url = "https://api.clearout.io/v2/email_verify/instant"
            payload = '{"email": email}'
            headers = {
                'Content-Type': "application/json",
                'Authorization': config.API_KEY,
                }
            res = requests.post(url, params=payload, headers=headers)
            res = res.json()
            print(email)
            print(res)
            if res["data"]["result"] == "valid":
                self.writeToCSV(firstName, lastName, company, domain, role, email)
                MongoFormatDAO.insertOne(domain, i)
                MongoUserDAO.insertOne(firstName, lastName, company, domain, role, email, False)    
            # elif res["result"] == "risky" or res["result"] == "unknown":
            #     self.writeToCSV(firstName, lastName, company, domain, role, email, "x")
            #     MongoUserDAO.insertOne(firstName, lastName, company, domain, role, email, True)    

        return False

    def checkForExistence(self, email):
        """
        Input: Prospective email
        Output: Boolean indicating whether this email has already been entered into the database
        """
        MongoUserDAO = MongoDAO.MongoUserDAO()
        res = MongoUserDAO.findByEmail({"email": email})
        if not res:
            return False
        res = list(res)
        if len(res) > 0:
            return True
        return False

    def checkForFormat(self, domain):
        """
        Input: Prospective domain
        Output: Format code of the email. If it doesn't exist, then returns False
        """
        MongoFormatDAO = MongoDAO.MongoFormatDAO()
        res = MongoFormatDAO.findByDomain(domain)
        if not res:
            return False
        res = list(res)
        if len(res) == 0:
            return False
        return res


    def writeToCSV(self, firstName, lastName, company, domain, role, email, tag=None):
        """
        Input: A series of values for a new prospect
        Output: None. The function just writes the client to the databse and writes to the databas
        """
        with open("Data/emails.csv", "a") as destinationFile:
            emailWriter = csv.writer(destinationFile)
            if tag:
                emailWriter.writerow([firstName + " " + lastName, company, domain, role, email, "x"])
            else:
                emailWriter.writerow([firstName + " " + lastName, company, domain, role, email])
        
    def convertCSV(self, fileName):
        """
        Input: A CSV file
        Output: None. The function just calls other functions to retrieve the email format and load into the database
        """

        with open(fileName) as sourceFile:
            emailReader = csv.reader(sourceFile)
            rowCount = sum(1 for row in emailReader)
            bar = progressbar.ProgressBar(maxval=rowCount).start()
        
        counter = 0
        with open(fileName) as sourceFile:
            emailReader = csv.reader(sourceFile)
            for i, row in enumerate(emailReader):
                firstName = row[0]
                lastName = row[1]
                company = row[2]
                domain = row[3]
                role = row[4]
                self.getEmailFormat(firstName, lastName, company, domain, role)
                counter += 1
                bar.update(counter)

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

        
