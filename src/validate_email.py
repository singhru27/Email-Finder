#!/usr/bin/python 
# _*_ coding:utf-8 _*_


import requests
import datetime


class MailtesterSingle():
   
    def __init__(self, key, email):
        self.key = key
        self.email = email
        self.verif = "https://api.mailtester.com/api/singlemail?secret="
        self.url = self.verif+self.key+"&email="+self.email

    
    def control(self):
        r = requests.get(self.url)
        return r.text


class MailtesterBulk():

    def __init__(self, key, user_file):
        datenow = datetime.datetime.now()
        self.key = key
        self.name = 'File' + datenow.strftime("%Y-%m-%d %H:%M")
        self.user_file = user_file
        self.url = 'https://api.mailtester.com/api/bulk?secret='+key+'&filename=%s' % self.name


    def upload(self):
        import pycurl
        
        infile = open('id_file', 'w')
        c = pycurl.Curl()
        c.setopt(c.POST, 1)
        c.setopt(c.URL, self.url)
        c.setopt(c.HTTPPOST, [('file_contents', (
                    c.FORM_FILE, self.user_file,
                    c.FORM_CONTENTTYPE, 'text/plain',
                    c.FORM_FILENAME, self.name.replace(' ','_'),)),])
        c.setopt(c.WRITEFUNCTION, infile.write)
        c.setopt(c.VERBOSE, 1)
        c.perform()
        c.close()


    def get_info(self):
       
        with open('id_file','r') as f:
            ids = f.read()
        url = 'https://api.mailtester.com/api/details?secret='+self.key+'&id=%s' % ids
        r = requests.get(url)
        with open('result.txt', 'a') as res:
            res.write(r.content+'\n')
