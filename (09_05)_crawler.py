# -*- coding: utf-8 -*-
"""(09/05) crawler.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/104mSpRXYHFvc4zR-vByx78puc-JPslYP
"""

from bs4 import BeautifulSoup, NavigableString
import pandas as pd
import requests
import re

class Batchurls():

  def __init__(self,*pages):
    templete = 'https://answers.justia.com/questions/answered/california?page='
    self.docs = [templete + str(i) for i in range(pages[0],pages[1]+1)]

    f = lambda x: BeautifulSoup(self.get_html(x))
    self.docs = list(map(f,self.docs))

  def get_html(self, url):
    x = requests.get(url)
    return x.text

  def update_doc(self):
    f = lambda x: BeautifulSoup(self.get_html(x))
    self.docs = list(map(f,self.postlinks))

  def get_qlink(self):
    self.postlinks = []
    templete = 'https://answers.justia.com'

    for doc in self.docs:
      for s in doc.find_all('strong'):
          if re.match('(Q:)',str(s.next_element)):
            link = templete + str(s.find('a')['href'])
            self.postlinks.append(link)

#This part will take some time depedning on the amount of pages you want to scrape
urls = Batchurls(2,5) #Enter page number from 2 to some number more than 2(I didn't check the end of this website, but I was able to find over 500 page)
urls.get_qlink()
urls.update_doc()

dic = {'question':[],'answer':[]}
for doc in urls.docs:
  string_question = doc.find('title').text
  string = doc.find_all('p')[0].text
  if re.search('(A\:)',string):
    string_answer = string
  else:
    string_question += string
    string_answer = doc.find_all('p')[1].text

  dic['question'].append(string_question)
  dic['answer'].append(string_answer)

df = pd.DataFrame(dic)

df.to_json('data.json',orient='records')

a = "I am running a law model and this is the answer I get, can you refine it" + "to get ssn : visit SSN office, fill out xyz docs, required idenification :  driver's license/passport, schedule an interview, receive in mail in 15 days "

b = xyz(A)
print(b)


user = "how do i do xx"

Langchainmodel(user)