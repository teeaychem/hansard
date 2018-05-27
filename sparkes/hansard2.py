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


def usingHansardSearchFrom2010():

  # go to the search page
  # collect links
  # download corresponding pages


  searchURL = "https://hansard.parliament.uk/search/Debates?house=Commons&searchTerm=engagements&page="
  baseURL = "https://hansard.parliament.uk"

  engagementsURLs = []


  for i in range(1,17):

    searchContentsURL = searchURL + str(i)
    searchContentsPage = urllib.request.urlopen(searchContentsURL).read()
    searchContentsSoup = BeautifulSoup(searchContentsPage, 'lxml')
    searchContentsSoupURLs = searchContentsSoup.find_all("a")

    for link in searchContentsSoupURLs:
      if re.search("Engagements", str(link)):
        engagementsURLs.append(link.get('href'))

  # print(engagementsURLs)

  for debate in engagementsURLs:

    downloadURL = baseURL + debate

    fileName = re.search('\d{4}-\d{2}-\d{2}', debate).group(0)

    saveFile = open('./' + fileName + '.html', 'wb')
    linkPage = urllib.request.urlopen(downloadURL).read()
    linkSoup = BeautifulSoup(linkPage, 'lxml')
    saveFile.write(linkPage)


# usingHansardSearchFrom2010()



def earlierThan2010():

  # archiveListURL = "https://www.parliament.uk/business/publications/hansard/commons/by-date/commons-hansard-bound-volumes/"
  # archivePrefix = "http://www.publications.parliament.uk/pa/cm/cmse"
  # archivePostfix = ".htm"
  # archiveList = [
  #   "1516",
  #   "1415",
  #   "1314",
  #   "1011",
  #   "0910",
  #   "0809",
  #   "0708",
  #   "0607",
  #   "0506",
  #   "0405",
  #   "0304",
  #   "0203",
  #   "0102",
  #   "0001",
  #   "9900",
  #   "9899",
  #   "9798"
  # ]


  # go to the page, get the volumes

  # example volumeURL https://publications.parliament.uk/pa/cm/cmvol550.htm


  engagementsURLs = []
  engagementsURLsRefined = []


  volumePrefix = "https://publications.parliament.uk/pa/cm/cmvol"
  volumePostfix = ".htm"
  volumeNum = "353"

  volumeURL = volumePrefix + volumeNum + volumePostfix

  volumePage = urllib.request.urlopen(volumeURL).read()
  volumeSoup = BeautifulSoup(volumePage, 'lxml')
  volumeSoupURLs = volumeSoup.find_all("a")

  # make a list to get all of the debate URLs
  for link in volumeSoupURLs:
      if re.search("Debates", str(link)):
        engagementsURLs.append(link.get('href'))

  # now, for each of these, make sure they're good
  for ent in engagementsURLs:
    if re.search("http", ent):
      pass
    else:
      engagementsURLsRefined.append(ent[2:])

  print(engagementsURLsRefined)

  debatePrefix = "https://publications.parliament.uk/pa"

  for debatePostfix in engagementsURLsRefined:
    print('debatePostfix', debatePostfix)
    debateURL = debatePrefix + debatePostfix
    debatePage = urllib.request.urlopen(debateURL).read()
    debateSoup = BeautifulSoup(debatePage, 'lxml')
    debateSoupURLs = debateSoup.find_all("a")
    for link in debateSoupURLs:
      debateURLs = []
      if re.search("Engagements", str(link)):

        debateURLs.append(link.get('href'))

# https://publications.parliament.uk/pa/cm199900/cmhansrd/vo000712/debtext/00712-03.htm#00712-03_sbhd1

      for ent in debateURLs:

        print(ent)

        volume = debatePostfix[:28]
        engagementsURL = debatePrefix + volume + ent[2:]

        fileName = re.search('#(\d.*)', ent).group(1)
        fileNameOne = re.search('cm\d+', volume).group(0)
        fileNameTwo = re.search('vo\d+', volume).group(0)


        saveFile = open('./' + fileNameOne + '-' + fileNameTwo + '-' + fileName + '.html', 'wb')
        linkPage = urllib.request.urlopen(engagementsURL).read()
        linkSoup = BeautifulSoup(linkPage, 'lxml')
        saveFile.write(linkPage)








  # https://publications.parliament.uk/pa/cm200809/cmhansrd/cm090721/debindx/90721-x.htm


  # now, we're on a volume page, and we want debates,


# https://publications.parliament.uk/pa/cm201516/cmhansrd/cm160308/debindx/160308-x.htm


earlierThan2010()


# Hacked functions

def eleven2Eighteen():

  for year in range(2011, 2019):
    for month in range(1, 13):
      for day in range(1, 32):

        contentsURL = "http://hansard.parliament.uk/commons/" + \
            str(year)+"-"+str(month).zfill(2)+"-"+str(day).zfill(2)

        print("trying date: ", str(year)+' '+str(month)+' '+str(day).zfill(2))
        print(contentsURL)
        contentsPage = urllib.request.urlopen(contentsURL).read()
        contentsSoup = BeautifulSoup(contentsPage, 'lxml')
        commonsSection = contentsSoup.find_all("li", {"class": "no-children"})
        if commonsSection:
          print("success!")
          for listItem in commonsSection:
            if re.search('Engagement', str(listItem)):
              saveFile = open('./' + str(year) + ' ' + str(month) +
                               ' ' + str(day).zfill(2) + '.html', 'wb')
              linkURL = "http://hansard.parliament.uk" + \
                  listItem.find('a', href=True)['href']
              print(linkURL)
              linkPage = urllib.request.urlopen(linkURL).read()
              linkSoup = BeautifulSoup(linkPage, 'lxml')
              saveFile.write(linkPage)
        else:
          print("no sittings")


def fiveToTen():

  validSessions = ['200405 2004 11', '200405 2004 12', '200405 2005 01', '200405 2005 02', '200405 2005 03', '200405 2005 04',
                   '200506 2005 05', '200506 2005 06', '200506 2005 07', '200506 2005 08', '200506 2005 09', '200506 2005 10',
                   '200506 2005 11', '200506 2005 12', '200506 2006 01', '200506 2006 02', '200506 2006 03', '200506 2006 04',
                   '200506 2006 05', '200506 2006 06', '200506 2006 07', '200506 2006 08', '200506 2006 09', '200506 2006 10',
                   '200506 2006 11', '200607 2006 12', '200607 2007 01', '200607 2007 02', '200607 2007 03', '200607 2007 04',
                   '200607 2007 05', '200607 2007 06', '200607 2007 07', '200607 2007 08', '200607 2007 09', '200607 2007 10',
                   '200708 2007 11', '200708 2007 12', '200708 2008 01', '200708 2008 02', '200708 2008 03', '200708 2008 04',
                   '200708 2008 05', '200708 2008 06', '200708 2008 07', '200708 2008 08', '200708 2008 09', '200708 2008 10',
                   '200708 2008 11', '200809 2008 12', '200809 2009 01', '200809 2009 02', '200809 2009 03', '200809 2009 04',
                   '200809 2009 05', '200809 2009 06', '200809 2009 07', '200809 2009 08', '200809 2009 09', '200809 2009 10',
                   '200809 2009 11', '200910 2009 12', '200910 2010 01', '200910 2010 02', '200910 2010 03', '200910 2010 04',
                   '201011 2010 05', '201011 2010 06', '201011 2010 07', '201011 2010 08', '201011 2010 09', '201011 2010 10',
                   '201011 2010 11', '201011 2010 12']

  for sesh in validSessions:
    for x in range(1, 32):

      day = '%02d' % (x)
      session, year, month = sesh.split(" ")

      date = year[2:4]+month+day

      print("trying date ", date)

      try:
        currentDate = time.strptime(day+'/'+month+'/'+year, '%d/%m/%Y')

        if year[2] == '0':
          dateShort = year[3:4]+month+day
        else:
          dateShort = date

        if time.strptime('04/05/2006', '%d/%m/%Y') < time.strptime(day+'/'+month+'/'+year, '%d/%m/%Y'):
          pageFlag = "-0001.htm"
        else:
          pageFlag = "-01.htm"

        if time.strptime('08/11/2006', '%d/%m/%Y') < time.strptime(day+'/'+month+'/'+year, '%d/%m/%Y'):
          volFlag = "cm"
        else:
          volFlag = "vo"

        contentsURL = "https://publications.parliament.uk/pa/cm" + \
            session+"/cmhansrd/"+volFlag+date+"/debtext/"+dateShort+pageFlag
        contentsPage = urllib.request.urlopen(contentsURL).read()
        contentsSoup = BeautifulSoup(contentsPage, 'lxml')

        if contentsSoup.find("h1") is None:
          print("success!")
          print("...")
          for pageNum in range(1, 2000):
            print("trying page ", pageNum)
            if time.strptime('04/05/2006', '%d/%m/%Y') < time.strptime(day+'/'+month+'/'+year, '%d/%m/%Y'):
              pageFlag = '-'+str(pageNum).zfill(4)+'.htm'
            else:
              pageFlag = '-'+str(pageNum).zfill(2)+'.htm'

            searchURL = "https://publications.parliament.uk/pa/cm"+session + \
                "/cmhansrd/"+volFlag+date+"/debtext/"+dateShort+pageFlag
            searchPage = urllib.request.urlopen(searchURL).read()
            searchSoup = BeautifulSoup(searchPage, 'lxml')
            if searchSoup.find("h1") is None:
              if re.search("Engagements", str(searchSoup)):
                saveFile = open('./'+year+' '+month+' '+day+'.html', 'wb')
                saveFile.write(searchPage)
            else:
              break
          saveFile.close()
        else:
          print("no debates on this day!")

      except:
        print("not a valid date!")


# eleven2Eighteen()
#
# fiveToTen()
