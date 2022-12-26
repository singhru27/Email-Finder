import csv
import config
import json
from validate_email import MailtesterSingle


class EmailWriter():
    def __init__(self):
        self.apiCounter = 0

    def getEmailFormat(self, firstName, lastName, company, domain, role):

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

        for email in emailList:
            self.apiCounter += 1
            E = MailtesterSingle(config.API_KEY, email)
            res = E.control()
            res = json.loads(res)
            print(email)
            print(res)
            if res["result"] == "valid":
                self.writeToCSV(firstName, lastName, company, domain, role, email)
                return True
            elif res["result"] == "unknown" or res["result"] == "risky":
                self.writeToCSV(firstName, lastName, company, domain, role, email, "x")
                return True

        return False

    def writeToCSV(self, firstName, lastName, company, domain, role, email, tag=None):

        with open("emails.csv", "a") as destinationFile:
            emailWriter = csv.writer(destinationFile)
            if tag:
                emailWriter.writerow([firstName + " " + lastName, company, domain, role, email, "x"])
            else:
                emailWriter.writerow([firstName + " " + lastName, company, domain, role, email])
        
    def convertCSV(self):
        with open("source.csv") as sourceFile:
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

if __name__ == "__main__":
    EmailWriter = EmailWriter()
    EmailWriter.convertCSV()
