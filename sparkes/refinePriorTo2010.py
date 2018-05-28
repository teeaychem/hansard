import codecs
import urllib
import os
import re
from bs4 import BeautifulSoup  # parses and searches HTML files
import fileinput

fileDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.dirname(fileDir)


# for file in os.listdir('../hansardBefore2010'):
#   localURL = 'file://' + os.path.join(parentDir, 'hansardBefore2010/' + file)


#   urllib.request.urlopen(localURL).read()
#   linkPage = urllib.request.urlopen(localURL).read()
#   linkSoup = BeautifulSoup(linkPage, 'html.parser')
#   # if linkSoup.find_all(string=re.compile('official engagements for')):
#   #   pass
#   # elif linkSoup.find_all(string=re.compile('Q\d')):
#   #   print(file)
#   # else:
#   #   # print(file)
#   #
#   if linkSoup.find_all(string=re.compile('(con)')):
#     pass
#   else:
#     print(file)
#     # pass




# for file in os.listdir('../hansardBefore2010'):
#   localURL = 'file://' + os.path.join(parentDir, 'hansardBefore2010/' + file)


#   urllib.request.urlopen(localURL).read()
#   linkPage = urllib.request.urlopen(localURL).read()
#   linkSoup = BeautifulSoup(linkPage, 'html.parser')
#   linkSoup = linkSoup.prettify(formatter="html")


#   linkSoup = re.sub(r'<notus.*\n?', '', linkSoup)
#   linkSoup = re.sub(r'</notus.*\n?', '', linkSoup)
#   linkSoup = re.sub(r'<b>\n[\w\s]+:\sColumn.*\n</b>\n?', '', linkSoup)
#   if re.sub(r'\s*[\w\s\d]+:\sColumn.*\n?', '', linkSoup):
#     linkSoup = re.sub(r'\s*[\w\s\d]+:\sColumn.*\n?', '', linkSoup)

#   saveFile = open(os.path.join(parentDir, 'hansardBefore2010ed/' + file), 'w')
#   saveFile.write(linkSoup)


def extractRelevantPartsOfBadHTMLFiles():
  foundCount = 0
  fileCount = 0

  for file in os.listdir('../hansardBefore2010'):
    # file = 'vol416-cm200304-vo040107-40107-03_sbhd2.html'
    fileLoc = os.path.join(parentDir, 'hansardBefore2010/' + file)
    with codecs.open(fileLoc, "rb", encoding="utf-8", errors='ignore') as f:

      saveFile = open(os.path.join(parentDir, 'hansardBefore2010txt/' + file + str(fileCount) + '.txt'), 'w')

      engageFlag = True
      found = False
      headSearch = False
      withinHead = True
      extraSearch = False
      gettingMeta = False
      for line in f:

        if re.findall(r'<(?:HEAD|head)>', line):
          gettingMeta = True
          extraSearch = True
        if re.findall(r'</(?:HEAD|head)>', line):
          gettingMeta = False
          engageFlag = False

        if gettingMeta == False:
          if re.findall(r'<[Hh]\d>(?:<[Cc]enter>|)Engagements', line):
            engageFlag = True
            found = True
            foundCount += 1
          elif re.findall(r'<[Hh]\d>(?:<[Cc]enter>|)\w+', line):
            engageFlag = False

          if engageFlag == False and (re.findall(r'<[Hh]\d', line) != None or headSearch == True):
            if headSearch == False:
              headSearch = True
            if re.findall(r'Engagements', line):
              engageFlag = True
              extraSearch = True
              withinHead = True
              found = True
              foundCount += 1
            if re.findall(r'</[Hh]\d>', line):
              withinHead = False
              headSearch = False
          if engageFlag == True and (re.findall(r'<[Hh]\d', line) != None) and withinHead == False:
            engageFlag == False


        if engageFlag == True or gettingMeta == True:
          if extraSearch == True:
            saveFile.write("%s\n" % line)

      if found == False:
        print(file)
      fileCount += 1
  print(foundCount)


def renamingTextFiles():

  fileCount = 0

  for file in os.listdir('../rawData/hansardBefore2010txt'):
    # file = 'vol416-cm200304-vo040107-40107-03_sbhd2.html'
    fileLoc = os.path.join(parentDir, 'rawData/hansardBefore2010txt/' + file)
    with codecs.open(fileLoc, "rb", encoding="utf-8", errors='ignore') as f:
      foundDate = False
      for line in f:
        if re.findall(r'name="Date"', line):
          # if foundDate == True:
          #   date2 = re.search(r'content(?:\s)*="((?:\d|\w|\s)+)"', line)
          #   if date2 == date:
          #     print('wft')
          #     print(date2)
          #     print(date)
          # foundDate = True
          dateRE = re.search(r'content(?:\s)*="((?:\d|\w|\s)+)"', line)
          date = dateRE.group(1)
      # if foundDate == False:
      #   print(file)

      # make sure each file gets a new name
      fileCount += 1

    with codecs.open(fileLoc, "rb", encoding="utf-8", errors='ignore') as f:
      saveFile = open(os.path.join(parentDir, 'rawData/hansardBefore2010txtdate/' + date + '-' + str(fileCount) + '.txt'), 'w')

      for line in f:
        # print(line)
        saveFile.write("%s\n" % line)









# extractRelevantPartsOfBadHTMLFiles()
# renamingTextFiles()