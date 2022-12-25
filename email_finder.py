import csv


class EmailWriter():
    def __init__(self):
        pass

    def getEmailFormat(self, firstName, lastName, domain):

        if not firstName or not lastName or not domain:
            return None

        emailList = []
        emailList.append(firstName + lastName + domain)
        emailList.append(firstName + "." + lastName + domain)
        emailList.append(firstName[0] + lastName + domain)
        emailList.append(firstName + lastName[0] + domain)
        emailList.append(firstName + domain)
        emailList.append(lastName + domain)
        emailList.append(firstName[0] + "." + lastName + domain)
        emailList.append(firstName + "." + lastName[0] + domain)
        emailList.append(lastName + firstName + domain)
        emailList.append(lastName + "." + firstName + domain)