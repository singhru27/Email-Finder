import csv
import config
from validate_email import MailtesterSingle


class EmailWriter():
    def __init__(self):
        pass

    def getEmailFormat(self, firstName, lastName, domain):

        if not firstName or not lastName or not domain:
            return None

        emailList = []
        emailList.append(firstName + lastName + "@" + domain)
        emailList.append(firstName + "." + lastName + "@" + domain)
        emailList.append(firstName[0] + lastName + "@" + domain)
        emailList.append(firstName[0] + "." + lastName + "@" + domain)
        emailList.append(lastName + firstName + "@" + domain)
        emailList.append(lastName + "." + firstName[0] + "@" + domain)
        emailList.append(firstName + "-" + lastName + "@" + domain)
        emailList.append(firstName + "_" + lastName + "@" + domain)
        emailList.append(firstName[0] + "_" + lastName + "@" + domain)
        emailList.append(firstName + lastName[0] + "@" + domain)
        emailList.append(lastName + "." + firstName + "@" + domain)
        emailList.append(firstName + "@" + domain)
        emailList.append(lastName + "@" + domain)
        emailList.append(firstName[0] + lastName[0] + "@" + domain)
        emailList.append(firstName + "." + lastName[0] + "@" + domain)
        emailList.append(lastName + firstName[0] + "@" + domain)
        emailList.append(lastName[0] + firstName + "@" + domain)
        emailList.append(lastName[0] + "." + firstName + "@" + domain)
        emailList.append(firstName[0] + "-" + lastName + "@" + domain)
        emailList.append(firstName + "-" + lastName[0] + "@" + domain)
        emailList.append(lastName + "-" + firstName + "@" + domain)
        emailList.append(lastName + "_" + firstName + "@" + domain)
        emailList.append(lastName[0] + "_" + firstName + "@" + domain)

        for email in emailList:
            print(email)
            E = MailtesterSingle(config.API_KEY, email)
            res = E.control()
            break
        
        return res


if __name__ == "__main__":
    EmailWriter = EmailWriter()
    print("Enter First Name")
    firstName = input()
    print("Enter Last Name")
    lastName = input()
    print("Enter Domain")
    domain = input()

    result = EmailWriter.getEmailFormat(firstName, lastName, domain)

    if result:
        print(result)
    else:
        print("No email found")