from __future__ import print_function

import re
import smtplib
import time

import requests
from bs4 import BeautifulSoup

username = 'XXXXX@gmail.com'
password = 'XXXXXX'
sender = 'XXXXXX@gmail.com'
receivers = ['XXXXXXXXX']


def getCities():
    '''
    Return a list of cities to search
    An empty list means to search everything
    Can be extended to read a file and return the list
    '''
    return ['Dallas', 'Irving', 'Roanoke']


def sendemail(listofstores1):
    message = """From: From XXXXX <XXXXXX@gmail.com>
            To: To Brad <XXXXX@vtext.com>
            Subject: Switch in stock
            """ + listofstores1

    try:
        smtpObj = smtplib.SMTP('smtp.gmail.com:587')
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login(username, password)
        smtpObj.sendmail(sender, receivers, message)
        return True
    except smtplib.SMTPException:
        return False


while True:
    result = ''
    cities = getCities()
    r = requests.get('http://www.istocknow.com/product/switch/system')
    soup = BeautifulSoup(r.content, 'html.parser')
    storelist = soup.find_all('a', class_='storename')
    for store in storelist:
        if "TX" in store.text:
            if cities:
                for city in cities:
                    if re.search(city, store.text, re.IGNORECASE):
                        result = result + "\n" + store.text
            else:
                result = result + "\n" + store.text
    if result is not '':
        sendemail(result)
        print("---")
        print(result)
    time.sleep(300)
