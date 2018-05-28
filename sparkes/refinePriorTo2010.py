import codecs
import urllib
import os
import re
from bs4 import BeautifulSoup  # parses and searches HTML files
import fileinput


def monStrToInt(month):
  monthInt = 0
  if month in 'January':
    monthInt = '01'
  elif month in 'February':
    monthInt = '02'
  elif month in 'March':
    monthInt = '03'
  elif month in 'April':
    monthInt = '04'
  elif month in 'May':
    monthInt = '05'
  elif month in 'June':
    monthInt = '06'
  elif month in 'July':
    monthInt = '07'
  elif month in 'August':
    monthInt = '08'
  elif month in 'September':
    monthInt = '09'
  elif month in 'October':
    monthInt = '10'
  elif month in 'November':
    monthInt = '11'
  elif month in 'December':
    monthInt = '12'
  return monthInt





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
        saveFile.write("%s\n" % line)


def getMetaData():

  for file in os.listdir('../rawData/hansardBefore2010txtdate'):

    fileLoc = os.path.join(parentDir, 'rawData/hansardBefore2010txtdate/' + file)

    with codecs.open(fileLoc, "rb", encoding="utf-8", errors='ignore') as f:
      metaVolume = False
      for line in f:
        if re.search(r'<meta.*content(?:\s*)=(?:\s*)"(H.*(?:\w|\s|\d|,|:)+)"', line):
          metaVolumeRE = re.search(r'<meta.*content(?:\s*)=(?:\s*)"(H.*(?:\w|\s|\d|,|:)+)"', line)
          metaVolume = metaVolumeRE.group(1)

      if metaVolume != False:
        print(metaVolume)
      else:
        print(file)


def cleanup():
  # this takes ages, unsurprisingly

  for file in os.listdir('../rawData/hansardBefore2010txtdate'):

    fileLoc = os.path.join(parentDir, 'rawData/hansardBefore2010txtdate/' + file)
    with codecs.open(fileLoc, "rb", encoding="utf-8", errors='ignore') as f:

      saveFile = open(os.path.join(parentDir, 'rawData/hansardBefore2010txtclean/' + file + '-clean-' + '.txt'), 'w')
      interestEnded = False
      for line in f:
        line = re.sub(r'.*\s*[\w\s\d]+:\sColumn.*\n?', '', line)
        line = re.sub(r'.*\s*<(?:html|HTML).*\n?', '', line)
        line = re.sub(r'.*\s*<(?:meta|META)\s*(?:name|NAME)\s*=\s*"(?:ObjectType|Publisher|Author|OtherAgent|Form|ISBN|Language|Identifier|Columns|Subject).*\n?', '', line)
        line = re.sub(r'.*\s*<(?:link|LINK)\s*(?:rel|REL)\s*=.*\n?', '', line)
        if re.search(r'>Next Section<', line):
          interestEnded = True
        if interestEnded == False and len(line.split()) > 0:
          saveFile.write("%s\n" % line)



def removeColumns():
  # could be incorporated with cleanup

   for file in os.listdir('../rawData/hansardBefore2010txtclean'):

    fileLoc = os.path.join(parentDir, 'rawData/hansardBefore2010txtclean/' + file)
    with codecs.open(fileLoc, "rb", encoding="utf-8", errors='ignore') as f:

      saveFile = open(os.path.join(parentDir, 'rawData/hansardBefore2010txtcleannew/' + file), 'w')
      for line in f:
        line = re.sub(r'.*<a\s*name\s*=\s*"(?:[Cc]olumn|COLUMN).*\n?', '', line)
        line = re.sub(r'<(?:/|)(?:[Pp]|BR|br|UL|ul)>\n?', '', line)
        line = re.sub(r'&nbsp;\n?', '', line)
        line = re.sub(r'<(?:head|HEAD)>\n?', '', line)
        line = re.sub(r'<(?:hr|HR)>\n?', '', line)
        line = re.sub(r'<(?:table|TABLE).*>\n?', '', line)
        if len(line.split()) > 0:
          saveFile.write("%s\n" % line)



def getQuestion():

  counter = 0

  for file in os.listdir('../rawData/hansardBefore2010txtcleannew'):

    if re.search(r'^\.', str(file)):
      pass
    else:

      fileLoc = os.path.join(parentDir, 'rawData/hansardBefore2010txtcleannew/' + file)
      questionTicker = 0

      with codecs.open(fileLoc, "rb", encoding="utf-8", errors='ignore') as f:

        fileRE = re.search(r'(\d+)\s(\w+) (\d{4})', str(file))
        day = fileRE.group(1)
        if len(day) == 1:
          day = '0' + day
        month = fileRE.group(2)
        year = fileRE.group(3)

        date = year + monStrToInt(month) + day

        questionDict = {
          '0':
            {
              "name" : "META",
              "date": date,
              "raw" : [],
              "comments" : [],
              "question": '',
              "a-tags" : [],
            }
          }

        for line in f:

          qLine = line

          if re.search(r'.*<[Bb]', line):
            name = "Unknown"
            if re.search(r'.*<[Bb]>\s*(\w(?:\w|\s|\.)+).*?<\/[Bb]>', line):
              name = re.search(r'.*<[Bb]>\s*(?:[Qq]|\d|\.|\s|\[|\])*(\w(?:\w|\s|\.)+).*?<\/[Bb]>', line)
              name = name.group(1).strip()
              name = re.sub(r'&#214;', 'Ö', name)
            questionTicker += 1
            questionDict[str(questionTicker)] = {}
            questionDict[str(questionTicker)]["name"] = name
            questionDict[str(questionTicker)]["date"] = date
            questionDict[str(questionTicker)]["question"] = ''
            questionDict[str(questionTicker)]["raw"] = []
            questionDict[str(questionTicker)]["a-tags"] = []
            questionDict[str(questionTicker)]["comments"] = []

            # print(name.group(1))
            counter += 1


          # preserve comments…
          if re.search(r'<!--.*?-->', line):
            comments = re.findall(r'<!--(.*?)-->', line)
            for comment in comments:
              questionDict[str(questionTicker)]["comments"].append(comment)

          # preserve a-tags
          if re.search(r'<\s*[Aa].*?[Aa]>', line):
            aTags = re.findall(r'<\s*[Aa](.*?)><\/[Aa]>', line)
            for aTag in aTags:
              questionDict[str(questionTicker)]["a-tags"].append(aTag)




          # removing things from the question
          # … but remove them from the raw text
          qLine = re.sub(r'(<!--.*?-->)', '', qLine)
          # also remove \n
          qLine = re.sub(r'\n', '', qLine)
          # and a-tags
          qLine = re.sub(r'<\s*[Aa](.*?)><\/[Aa]>', '', qLine)
          # and b-tags
          qLine = re.sub(r'</*[Bb]>', '', qLine)
          # and i-tags
          qLine = re.sub(r'</*[Ii]>', '', qLine)
          # and font changes
          qLine = re.sub(r'</*\s*(?:font|FONT).*?>', '', qLine)
          # at this point, a few tags remain in questions, but these are only for the PM, and so can be ignored.

          # Now, let's clean up the html
          qLine = re.sub(r'&#(?:039|145|146);', '\'', qLine)
          qLine = re.sub(r'&(?:quot|#147|#148);', '\"', qLine)
          qLine = re.sub(r'&#150;', ' – ', qLine)
          qLine = re.sub(r'&#151;', ' — ', qLine)
          qLine = re.sub(r'&#163;', '£', qLine)
          qLine = re.sub(r'&#8364;', '€', qLine)
          qLine = re.sub(r'&#233;', 'é', qLine)
          qLine = re.sub(r'&#237;', 'í', qLine)
          qLine = re.sub(r'&#226;', 'â', qLine)
          qLine = re.sub(r'&#244;', 'ô', qLine)
          qLine = re.sub(r'&#246;', 'ö', qLine)
          qLine = re.sub(r'&#214;', 'Ö', qLine)
          qLine = re.sub(r'&#224;', 'à', qLine)
















          if len(qLine) > 0:
            questionDict[str(questionTicker)]["question"] += qLine



          questionDict[str(questionTicker)]["raw"].append(line)






          # input('x')
      if questionTicker == False:
        print(file)
      print(file)
      for item in questionDict.keys():
        if questionDict[item]['name'] == "META":
          pass
        else:
          print('~~~~~~~' + file)
          print('name: ' + questionDict[item]['name'])
          print('date: ' + questionDict[item]['date'])
          print('question:')
          print(questionDict[item]['question'])

        # for key in questionDict[item].keys():
        #   print(key + ':')
        #   print('\n')
        #   print(questionDict[item][key])
        #   print('\n')

      # # input('x')
    print(counter)



"""
  Misc code
"""

#   name = re.search(r'.*<[Bb]>(.*)</[Bb]>', line)
#   if re.search(r'(?:Prime|Speaker)', name.group(1)) == None:
# if re.search(r'.*<[Aa]\s+(?:name|NAME)\s*=\s*"', line):
#   if re.search(r'(?:meta|META)\s*(?:name|NAME)\s*=\s*"[Ss]peaker', line) == None:


"""
  Run specific functions
"""
# extractRelevantPartsOfBadHTMLFiles()
# renamingTextFiles()
# getMetaData()
getQuestion()
# cleanup()
# removeColumns()