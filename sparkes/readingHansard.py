import urllib  # requests and grabs information from web pages
from bs4 import BeautifulSoup  # parses and searches HTML files
import matplotlib.pyplot as plt  # plots results
import matplotlib
import re  # uses regular expressions to efficiently search large bodies of text
import pickle  # allows export of dictionaries and facilitates pickle rick jokes
from collections import Counter  # rapidly parses dictionaries
import os
import math
import time
from glob import glob
import calendar
from datetime import datetime
import re

fileDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.dirname(fileDir)
localURL = 'file:///' + os.path.join(parentDir, 'hansard2010to2018/2010-03-10.html')

# print(os.listdir('../hansard2010to2018'))

globalMemberDict = {
  "Edward Miliband" : ["Lab", "Doncaster North"],
  "Jeremy Corbyn" : ["Lab", "Islington North"],
  "Damian Green" : ["Con", "Ashford"],
  "Angus Robertson": ["SNP", "Moray"],
  "David Lidington" : ["Con", "Aylesbury"],
  "Harriet Harman" : ["Lab", "Camberwell and Peckham"],
  "George Osborne": ["Con", "Tatton"],
  "William Hague" : ["Con", "Richmond"],
  "Chris Grayling": ["Con", "Epsom and Ewell"],
  "Michael Connarty": ["Lab", "Linlithgow and East Falkirk"]
}

totalStuff = set([])

globalList = globalMemberDict.keys()


memberDict = {}

for file in os.listdir('../hansard2010to2018'):
  localURL = 'file://' + os.path.join(parentDir, 'hansard2010to2018/' + file)
  # print(localURL)

  urllib.request.urlopen(localURL).read()
  linkPage = urllib.request.urlopen(localURL).read()
  linkSoup = BeautifulSoup(linkPage, 'html.parser')
  # print(linkSoup)
  # saveFile.write(linkPage)

  localDict = {}
  localList = []

  for q in linkSoup.find_all('li'):
        n = q.find('a', title="View member's contributions")
        if n is None:
            pass
        else:
            if 'Prime Minister' in n.text or 'Speaker' in n.text:
                pass
            else:
                # Get the member's name
                name = n.text

                # Extract the party
                # print(re.findall(r'[^\(]*\([^\)]*\) ?\(([^\)]*)\)', name)[0])

                # Get the question asked
                # q_div = q.find('div', class_="contribution col-md-9")
                question = ''
                for p in q('p'):
                    question += p.text

                # Is it a follow-up?

                # Get the URL
                url = ''
                for u in q('a', title="Share this contribution"):
                    url = u.get('data-hop-popover')

                member = re.search(r'([^\(]*)\s+\(([\w\s\(\)\,-]+?)\)\s+?\(([^\)]*)\)', n.text)
                memSurnameRE = re.search(r'^(?:Mr|Mrs|Ms|Dr)[\. ]+(\w[\w ]+)', n.text)
                memMinisterRE = re.search(r'\((?:\w+ )+(\w+)\)$', n.text)
                memName = False
                if member:
                  memName = member.group(1)
                  memCons = member.group(2)
                  memPart = member.group(3)
                  localList.append(memName)
                  localDict[memName] = [memPart, memCons]
                elif memSurnameRE:
                  memSurname = memSurnameRE.group(1)
                  for item in localList:
                    if memSurname in item:
                      memName = item
                      memPart = localDict[memName][0]
                      memCons = localDict[memName][1]
                  if memName == False:
                    for item in globalList:
                      if memSurname in item:
                        memName = item
                        memPart = globalMemberDict[memName][0]
                        memCons = globalMemberDict[memName][1]
                elif n.text in localList:
                  memName = n.text
                  memPart = localDict[memName][0]
                  memCons = localDict[memName][1]
                  pass
                elif n.text in globalList:
                  memName = n.text
                  memPart = globalMemberDict[memName][0]
                  memCons = globalMemberDict[memName][1]
                elif memMinisterRE:
                  name = memMinisterRE.group(1)
                  for item in globalList:
                    if name in item:
                      memName = item
                      memPart = globalMemberDict[memName][0]
                      memCons = globalMemberDict[memName][1]
                else:
                  pass

                if memName != False:
                  # don't add to results
                  pass
                  totalStuff.add(str([memName, memPart, memCons, localURL]))


for item in totalStuff:
  print(item)

                #   memberDict[member.group(1)] = {"party" : member.group(3), "constituency" :  member.group(2)}

                  # print(name)
                  # print(member.group(1))
                  # print(member.group(2))
                  # print(member.group(3))

                # Print what we've got so far

                # print(question)
                # print(url)
  # print(memberDict)
  # input("Press Enter to continue...")
# print(memberDict)
# for item in memberDict.keys():
#   print(len(memberDict[item]))
#   print(memberDict[item]['party'])
