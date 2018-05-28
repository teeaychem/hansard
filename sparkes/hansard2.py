import urllib  # requests and grabs information from web pages
from bs4 import BeautifulSoup  # parses and searches HTML files
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



def earlierThan2010before453(volnum):

  # go to the page, get the volumes

  # example volumeURL https://publications.parliament.uk/pa/cm/cmvol550.htm


  if int(volnum) > 452:
    print('won\'t fly')
  else:

    engagementsURLs = []
    engagementsURLsRefined = []


    volumePrefix = "https://publications.parliament.uk/pa/cm/cmvol"
    volumePostfix = ".htm"
    volumeNum = volnum

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
        ent = re.sub(r'\n', '', ent)
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
          if re.search('cm\d+', volume):
            fileNameOne = re.search('cm\d+', volume).group(0)
          else:
            fileNameOne = re.search('\d+', volume).group(1)
          if re.search('vo\d+', volume):
            fileNameTwo = re.search('vo\d+', volume).group(0)
          else:
            fileNameTwo = 'vol' + volnum


          saveFile = open('../before2010/' + 'vol' + volnum + '-' + fileNameOne + '-' + fileNameTwo + '-' + fileName + '.html', 'wb')
          linkPage = urllib.request.urlopen(engagementsURL).read()
          linkSoup = BeautifulSoup(linkPage, 'lxml')
          saveFile.write(linkPage)

    # https://publications.parliament.uk/pa/cm200809/cmhansrd/cm090721/debindx/90721-x.htm


    # now, we're on a volume page, and we want debates,


  # https://publications.parliament.uk/pa/cm201516/cmhansrd/cm160308/debindx/160308-x.htm


# for i in range(453, 502):
#   print(str(i))
#   earlierThan2010before453(str(i))


def earlierThan2010after453(volnum):

  # go to the page, get the volumes

  # example volumeURL https://publications.parliament.uk/pa/cm/cmvol550.htm


  if int(volnum) < 453:
    print('use the other function')
  else:

    engagementsURLs = []
    engagementsURLsRefined = []


    volumePrefix = "https://publications.parliament.uk/pa/cm/cmvol"
    volumePostfix = ".htm"
    volumeNum = volnum

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
        ent = re.sub(r'\n', '', ent)
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
          engagementsURL = debatePrefix + ent[3:]
          print(engagementsURL)

          fileName = re.search('#(\d.*)', ent).group(1)
          if re.search('cm\d+', volume):
            print(re.findall('cm\d+', volume))
            fileNameOne = re.findall('cm\d+', volume)[1]
          else:
            fileNameOne = re.search('\d+', volume).group(1)
          if re.search('vo\d+', volume):
            fileNameTwo = re.search('vo\d+', volume).group(0)
          else:
            fileNameTwo = 'vol' + volnum


          saveFile = open('../before2010/' + 'vol' + volnum + '-' + fileNameOne + '-' + fileNameTwo + '-' + fileName + '.html', 'wb')
          linkPage = urllib.request.urlopen(engagementsURL).read()
          linkSoup = BeautifulSoup(linkPage, 'lxml')
          saveFile.write(linkPage)

    # https://publications.parliament.uk/pa/cm200809/cmhansrd/cm090721/debindx/90721-x.htm


    # now, we're on a volume page, and we want debates,


  # https://publications.parliament.uk/pa/cm201516/cmhansrd/cm160308/debindx/160308-x.htm


# for i in range(498, 502):
#   print(str(i))
#   earlierThan2010after453(str(i))

# Note, interal server error on 497

engagementsURL = 'https://publications.parliament.uk/pa/cm200809/cmhansrd/cm091014/debindx/91014-x.htm'
saveFile = open('../before2010/' + 'cm200809-cmhansrd-cm091014-debindx-91014-x.htm', 'wb')
linkPage = urllib.request.urlopen(engagementsURL).read()
linkSoup = BeautifulSoup(linkPage, 'lxml')
saveFile.write(linkPage)

engagementsURL = 'https://publications.parliament.uk/pa/cm200809/cmhansrd/cm091021/debindx/91021-x.htm'
saveFile = open('../before2010/' + 'cm200809-cmhansrd-cm091021-debindx-91021-x.htm', 'wb')
linkPage = urllib.request.urlopen(engagementsURL).read()
linkSoup = BeautifulSoup(linkPage, 'lxml')
saveFile.write(linkPage)

engagementsURL = 'https://publications.parliament.uk/pa/cm200809/cmhansrd/cm091014/debtext/91014-0002.htm'
saveFile = open('../before2010/' + 'cm200809-cmhansrd-cm091014-debtext-91014-0002.htm', 'wb')
linkPage = urllib.request.urlopen(engagementsURL).read()
linkSoup = BeautifulSoup(linkPage, 'lxml')
saveFile.write(linkPage)