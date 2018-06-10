import codecs
import urllib
import os
import re
from bs4 import BeautifulSoup  # parses and searches HTML files
import fileinput
import csv
import pickle


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

  bigQList = []

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


      bigQList.append(questionDict)

      # input('x')
    #   if questionTicker == False:
    #     print(file)
    #   print(file)
    #   for item in questionDict.keys():
    #     if questionDict[item]['name'] == "META":
    #       pass
    #     else:
    #       print('~~~~~~~ ' + file + ' ~~~~~~~')
    #       print('name: ' + questionDict[item]['name'])
    #       print('date: ' + questionDict[item]['date'])
    #       print('question:')
    #       print(questionDict[item]['question'])

    #     # for key in questionDict[item].keys():
    #     #   print(key + ':')
    #     #   print('\n')
    #     #   print(questionDict[item][key])
    #     #   print('\n')

    #   # input('x')
    # print(counter)
  return bigQList

# Run this to output a list of dictionaries, each dictionary corresponding to a file
# bigQList = getQuestion()

# We now save this so that we don't have to wait each time
# pickle.dump( bigQList, open( "../data/basic1992000data.p", "wb" ) )
# And so instead of running getQuestions() we load…



def updateBasicData():

  counter = 0
  lost = 0

  ugh = set([])
  finalQs = []

  globalDict = {
    "Harriet Harman" : ["Camberwell and Peckham", "Lab"],
    "Menzies Campbell" : ["North East Fife", "LD"], "Colin Challen" : ["Morley and Rothwell", "Lab"], "Chris Grayling": ["Epsom and Ewell", "Con"], "Harry Cohen": ["Leyton and Wanstead", "Lab"], "Colin Burgon": ["Elmet", "Lab"], "Linda Perham": ["Ilford North", "Lab"], "Gerald Kaufman": ["Manchester Ardwick/Gorton", "Lab"], "Jeremy Corbyn": ["Islington North", "Lab"], "Michael Spicer": ["West Worcestershire", "Con"], "Patrick Hall": ["Bedford", "Lab"], "Michael Howard": ["Folkestone and Hythe", "Con"], "David Cameron": ["Witney", "Con"], "William Hague" : ["Richmond", "Con"], "Geoff Hoon": ["Ashfield", "Lab"], "Nick Clegg": ["Sheffield Hallam", "LD"], "Bob Marshall-Andrews": ["Medway", "Lab"], "Charles Kennedy": ["Ross, Skye and Lochaber", "LD"], "Iain Duncan Smith": ["Chingford and Woodford Green", "Con"], "Michael Ancram": ["Devizes", "Con"], "Edward Heath":["Old Bexley and Sidcup", "Con"], "Henry Bellingham": ["North West Norfolk", "Con"], "Karl Turner": ["Kingston upon Hull East", "Lab"], "Brian Binley": ["Northampton South", "Con"], "Andrew Griffiths": ["Burton", "Con"], "Owen Paterson": ["North Shropshire", "Con"], "John Leech": ["Manchester, Withington", "LD"], "Alistair Carmichael": ["Orkney and Shetland", "LD"], "Peter Luff":["Mid Worcestershire", "Con"], "Graham Allen": ["Nottingham North", "Lab"], "Ben Chapman": ["Wirral South", "Lab"], "Andrew Murrison": ["South West Wiltshire", "Con"], "Richard Bacon": ["South Norfolk", "Con"], "Iain Luke": ["Dundee East", "Lab"], "Dennis Skinner": ["Bolsover", "Lab"], "Gordon Marsden": ["Blackpool South", "Lab"], "John Wilkinson": ["Ruislip-Northwood", "Con"], "Robin Cook": ["Livingston", "Lab"], "Eric Forth": ["Bromley and Chislehurst", "Con"], "George Young": ["North West Hampshire", "Con"], "Geoffrey Clifton-Brow": ["Cotswold", "Con"], "Angela Browning": ["Tiverton and Honiton", "Con"], "John Michael Jack": ["Fylde", "Con"], "Tim Loughton": ["East Worthing and Shoreham", "Con"], "Angela Watkinson": ["Upminster", "Con"], "Simon Burns": ["West Chelmsford", "Con"], "Gerald Howarth": ["Aldershot", "Con"], "Ann Winterton": ["Congleton", "Con"], "Richard Ottaway": ["Croydon, South", "Con"], "Michael Fabricant": ["Lichfield", "Con"], "Chris Bryant": ["Rhondda", "Lab"], "Fiona Mactaggart": ["Slough", "Lab"], "Jim Sheridan": ["Paisley and Renfrewshire, North", "Lab"], "John Robertson": ["Glasgow, North-West", "Lab"], "Kali Mountford": ["Colne Valley", "Lab"], "Peter Bradley": ["The Wrekin)", "Lab"], "Paddy Tipping": [ "Sherwood", "Lab"], "Ann Clwyd": ["Cynon Valley", "Lab"], "Cable": ["Twickenham", "LD"], "Clarke": ["Coatbridge, Chryston and Bellshill", "Lab"], "Salter": ["Reading, West", "Lab"], "Miller": ["Ellesmere Port and Neston", "Lab"], "Taylor": ["Rochford and Southend, East", "Con"], "Keeble": ["Northampton, North", "Lab"], "King": ["Kingswood", "Lab"], "Hughes": ["North Southwark and Bermondsey", "LD"], "Starkey": ["Milton Keynes, South-West", "Lab"], "Foster": ["Hastings and Rye", "Lab"], "Naysmith": ["Bristol, North-West", "Lab/Co-op"], "Harris": ["Glasgow, South", "Lab"], "Leigh": ["Gainsborough", "Con"], "Blunt": ["Reigate", "Con"], "Kidney": ["Stafford", "Lab"], "Prosser": ["Dover", "Lab"], "Hamilton": ["Leeds, North-East", "Lab"], "Gardiner": ["Brent, North", "Lab"], "Jenkins": ["Tamworth", "Lab"], "Garnier": ["Harborough", "Con"], "Beith": ["Berwick-upon-Tweed", "LD"], "Hayes": ["Hayes and Harlington", "Lab"], "McDonnell": ["Hayes and Harlington", "Lab"], "Purchase": ["Wolverhampton, North-East", "Lab/Co-op"], "Blizzard": ["Waveney", "Lab"], "Green": ["Ryedale", "Con"], "Greenway": ["Ryedale", "Con"], "Brady": ["Altrincham and Sale, West", "Con"], "Heathcoat": ["Wells", "Con"], "Havard": ["Merthyr Tydfil and Rhymney", "Lab"], "Salmond": ["Banff and Buchan", "SNP"], "Donohoe": ["Central Ayrshire", "Lab"], "Cash": ["Stone", "Con"], "Gibson": ["Norwich, North", "Lab"], "Illsley": ["Barnsley, Central", "Lab"], "Bercow": ["Buckingham", "Con"], "Robathan": ["Blaby", "Con"], "Cunningham": ["Coventry, South", "Lab"], "Tami": ["Alyn and Deeside", "Lab"], "Amess": ["Southend, West", "Con"], "Heppell": ["Nottingham, East", "Lab"], "Bottomley": ["Worthing, West", "Con"], "Winnick": ["Walsall, North", "Lab"], "Moffatt": ["Crawley", "Lab"], "Thomas": ["Crosby", "Lab"], "Brooke": ["Mid-Dorset and North Poole", "LD"], "Gilroy": ["Plymouth, Sutton", "Lab/Co-op"], "Prisk": ["Hertford and Stortford", "Con"], "McFall": ["West Dunbartonshire", "Lab/Co-op"], "Jackson": ["Peterborough", "Con"], "Brazier": ["Canterbury", "Con"], "Beresford": ["Mole Valley", "Con"], "Wyatt": ["Sittingbourne and Sheppey", "Lab"], "Barker": ["Bexhill and Battle", "Con"], "Crausby": ["Bolton, North-East", "Lab"], "Doughty": ["Cardiff South and Penarth", "Lab/Co-op"], "Goggins": ["Wythenshawe and Sale East", "Lab"], "Chope": ["Christchurch", "Con"], "Bradshaw": ["Exeter", "Lab"], "Burstow": ["Sutton and Cheam", "LD"], "Hendry": ["Inverness, Nairn, Badenoch and Strathspey", "SNP"], "Munn": ["Sheffield, Heeley", "Lab/Co-op"], "McCabe": ["Birmingham, Selly Oak", "Lab"], "Ward": ["Bradford East", "LD"], "Harvey": ["North Devon", "LD"], "Clappison": ["Hertsmere", "Con"], "Edwards": ["Carmarthen East and Dinefwr", "PC"], "Mullin": ["Kirkcaldy and Cowdenbeath", "SNP"], "Anderson": ["Blaydon", "Lab"], "Hammond": ["Wimbledon", "Con"], "Norris": ["Nottingham North", "Lab/Co-op"], "Sawford": ["Corby", "Lab/Co-op"], "Paice": ["South East Cambridgeshire", "Con"],
    # For getting party with cons, prior to 2010
    'Robinson': ['Strangford', 'DUP'], 'Cormack': ['South Staffordshire', 'Con'],'Swire': ['East Devon', 'Con'],'McGrady': ['South Down', 'SDLP'],'Mahmood': ['Birmingham, Perry Barr', 'Lab'],'Connarty': ['Linlithgow and East Falkirk', 'Lab'], 'McKenna': ['Cumbernauld, Kilsyth and Kirkintilloch, East', 'Lab'], 'Lazarowicz': ['Edinburgh, North and Leith', 'Lab/Co-op'], 'White': ['Southampton, Test', 'Lab'], 'Whitehead': ['Southampton, Test', 'Lab'], 'Begg': ['Aberdeen, South', 'Lab'], 'Buck': ['Buckingham', 'Con'], 'Blackman': ['City of Durham', 'Lab'], 'Llwyd': ['Meirionnydd Nant Conwy', 'PC'], 'Gillan': ['Chesham and Amersham', 'Con'], 'Gill': ['Chesham and Amersham', 'Con'], 'Spink': ['Castle Point', 'Ind'], 'Caton': ['Gower', 'Lab'], 'Davey': ['Bristol, West', 'Lab'], 'Lembit': ['Montgomeryshire', 'LD'], 'Selous': ['South-West Bedfordshire', 'Con'], 'Baron': ['Billericay', 'Con'], 'Dodds': ['Belfast, North', 'DUP'], 'Dismore': ['Hendon', 'Lab'], 'Simpson': ['Upper Bann', 'DUP'], 'Tapsell': ['Louth and Horncastle', 'Con'], 'Humble': ['Blackpool, North and Fleetwood', 'Lab'], 'Rosindell': ['Romford', 'Con'], 'Reed': ['Loughborough', 'Lab/Co-op'], 'Palmer': ['Broxtowe', 'Lab'], 'Mann': ['Bassetlaw', 'Lab'], 'Ellman': ['Liverpool, Riverside', 'Lab/Co-op'], 'Soames': ['Mid-Sussex', 'Con'], 'Jones': ['North Durham', 'Lab'], 'Vaz': ['Leicester, East', 'Lab'], 'Gapes': ['Ilford, South', 'Lab/Co-op'], 'Stoate': ['Dartford', 'Lab'], 'Mitchell': ['Sutton Coldfield', 'Con'], 'Davidson': ['Glasgow, South-West', 'Lab/Co-op'], 'Waterson': ['Eastbourne', 'Con'], 'Hood': ['Lanark and Hamilton, East', 'Lab'], 'Ennis': ['Barnsley, East and Mexborough', 'Lab'], 'McIntosh': ['Vale of York', 'Con'], 'Paisley': ['Paisley and Renfrewshire, North', 'Lab'], 'Reid': ['Argyll and Bute', 'LD'], 'Lidington': ['Aylesbury', 'Con'], 'Berry': ['Kingswood', 'Lab'], 'Hoyle': ['Chorley', 'Lab'], 'Francis': ['Horsham', 'Con'], 'Randall': ['Uxbridge', 'Con'], 'Madel': ['Bridgend', 'Lab'], 'Russell': ['Dumfries and Galloway', 'Lab'], 'Borrow': ['South Ribble', 'Lab'], 'Walley': ['Stoke-on-Trent, North', 'Lab'], 'McIsaac': ['Cleethorpes', 'Lab'], 'Clapham': ['Barnsley, West and Penistone', 'Lab'], 'Lewis': ['New Forest, East', 'Con'], 'Mole': ['Mole Valley', 'Con'], 'McCafferty': ['Calder Valley', 'Lab'], 'Wishart': ['Perth and North Perthshire', 'SNP'], 'Burden': ['Birmingham, Northfield', 'Lab'], 'Bruce': ['Gordon', 'LD'], 'Stuart': ['Beverley and Holderness', 'Con'], 'Mackay': ['Bracknell', 'Con'], 'Lucas': ['Wrexham', 'Lab'], 'House': ['Totnes', 'Con'], 'Ryan': ['Enfield, North', 'Lab'], 'Conway': ['Old Bexley and Sidcup', 'Con'], 'Pound': ['Ealing, North', 'Lab'], 'Barron': ['Rother Valley', 'Lab'], 'Steen': ['Totnes', 'Con'], 'Roy': ['Glenrothes', 'Lab'], 'Wright': ['Cannock Chase', 'Lab'], 'Wiggin': ['Leominster', 'Con'], 'Bayley': ['City of York', 'Lab'], 'Streeter': ['South-West Devon', 'Con'], 'Ruane': ['Vale of Clwyd', 'Lab'], 'Morgan': ['Cardiff, North', 'Lab'], 'McKechin': ['Glasgow, North', 'Lab'], 'Evans': ['Ribble Valley', 'Con'], 'Williams': ['Caernarfon', 'PC'], 'Hepburn': ['Jarrow', 'Lab'], 'Curtis': ['Crosby', 'Lab'], 'Kumar': ['Middlesbrough, South and East Cleveland', 'Lab'], 'Stunell': ['Hazel Grove', 'LD'], 'Maples': ['Stratford-on-Avon', 'Con'], 'Shipley': ['Shipley', 'Con'], 'Davies': ['Monmouth', 'Con'], 'Hoey': ['Vauxhall', 'Lab'], 'Stringer': ['Manchester, Blackley', 'Lab'], 'Gale': ['North Thanet', 'Con'], 'Cryer': ['Keighley', 'Lab'], 'Todd': ['South Derbyshire', 'Lab'], 'Levitt': ['High Peak', 'Lab'], 'Meacher': ['Oldham, West and Royton', 'Lab'], 'Atkins': ['Staffordshire, Moorlands', 'Lab'], 'Joyce': ['Falkirk', 'Lab'], 'Barrett': ['Edinburgh, West', 'LD'], 'Donaldson': ['Lagan Valley', 'DUP'], 'Sarwar': ['Glasgow, Central', 'Lab'], 'Osborne': ['Ayr, Carrick and Cumnock', 'Lab'], 'Weir': ['Angus', 'SNP'], 'Wood': ['Hornsey and Wood Green', 'LD'], 'Widdecombe': ['Maidstone and The Weald', 'Con'], 'Banks': ['Ochil and South Perthshire', 'Lab'], 'Webb': ['Northavon', 'LD'], 'Cawsey': ['Brigg and Goole', 'Lab'], 'Rowe': ['Rochdale', 'LD'], 'Grogan': ['Selby', 'Lab'], 'Martlew': ['Carlisle', 'Lab'], 'Bailey': ['West Bromwich, West', 'Lab/Co-op'], 'Twigg': ['Halton', 'Lab'], 'Stewart': ['Dundee, East', 'SNP'], 'Gidley': ['Romsey', 'LD'], 'Lloyd': ['Manchester, Central', 'Lab'], 'Norman': ['Lewes', 'LD'], 'Baker': ['Lewes', 'LD'], 'Dhanda': ['Gloucester', 'Lab'], 'Sanders': ['Torbay', 'LD'], 'Prentice': ['Pendle', 'Lab'], 'Follett': ['Stevenage', 'Lab'], 'Linton': ['Battersea', 'Lab'], 'Laing': ['Epping Forest', 'Con'], 'Mates': ['East Hampshire', 'Con'], 'MacShane': ['Rotherham', 'Lab'], 'Butterfill': ['Bournemouth, West', 'Con'], 'Flynn': ['Newport, West', 'Lab'], 'Price': ['Carmarthen, East and Dinefwr', 'PC'], 'Southworth': ['Warrington, South', 'Lab'], 'Chaytor': ['Bury, North', 'Lab'], 'Francois': ['Rayleigh', 'Con'], 'Heal': ['North-East Hertfordshire', 'Con'], 'Spring': ['West Suffolk', 'Con'], 'Farrelly': ['Newcastle-under-Lyme', 'Lab'], 'Grant': ['Grantham and Stamford', 'Lab'], 'Simmonds': ['Boston and Skegness', 'Con'], 'Younger': ['Teignbridge', 'LD'], 'Galloway': ['Dumfries and Galloway', 'Lab'], 'Baldry': ['Banbury', 'Con'], 'Hopkins': ['Luton, North', 'Lab'],
    # For getting party with cons, from 2010 to 2018
    'Ruffley': ['Bury St Edmunds', 'Con'], 'Leslie': ['Bristol North West', 'Con'], 'Adams': ['Selby and Ainsty', 'Con'], 'Ruddock': ['Lewisham, Deptford', 'Lab'], 'Plaskitt': ['Warwick and Leamington', 'Lab'], 'Redwood': ['Wokingham', 'Con'], 'Quin': ['Horsham', 'Con'], 'Johnson': ['Kingston upon Hull North', 'Lab'], 'Irranca': ['Ogmore', 'Lab'], 'Abbott': ['Hackney North and Stoke Newington', 'Lab'], 'Lammy': ['Tottenham', 'Lab'], 'Davis': ['Haltemprice and Howden', 'Con'], 'Cairns': ['Vale of Glamorgan', 'Con'], 'Dobbin': ['Heywood and Middleton', 'Lab/Co-op'], 'Stevenson': ['Carlisle', 'Con'], 'Flint': ['Don Valley', 'Lab'], 'Lansley': ['South Cambridgeshire', 'Con'], 'Brennan': ['Cardiff West', 'Lab'], 'Collins': ['Folkestone and Hythe', 'Con'], 'Efford': ['Eltham', 'Lab'], 'McDonagh': ['Mitcham and Morden', 'Lab'], 'Knight': ['Solihull', 'Con'], 'Mercer': ['Plymouth, Moor View', 'Con'], 'Allan': ['Telford', 'Con'], 'Sheerman': ['Huddersfield', 'Lab/Co-op'], 'Coaker': ['Gedling', 'Lab'], 'Eagle': ['Wallasey', 'Lab'], 'Hancock': ['West Suffolk', 'Con'], 'Brake': ['Carshalton and Wallington', 'LD'], 'Watson': ['West Bromwich East', 'Lab'], 'Mackinlay': ['South Thanet', 'Con'], 'Moran': ['Oxford West and Abingdon', 'LD'], 'Benn': ['Leeds Central', 'Lab'], 'Singh': ['Slough', 'Lab'], 'Swayne': ['New Forest West', 'Con'], 'Smyth': ['Bristol South', 'Lab'], 'Blears': ['Salford and Eccles', 'Lab'], 'Lamb': ['North Norfolk', 'LD'], 'Day': ['Linlithgow and East Falkirk', 'SNP'], 'Burnham': ['Leigh', 'Lab'], 'Lilley': ['Hitchin and Harpenden', 'Con'], 'Spelman': ['Meriden', 'Con'], 'Gummer': ['Ipswich', 'Con'], 'Browne': ['Taunton Deane', 'LD'], 'Arbuthnot': ['North East Hampshire', 'Con'], 'Mahon': ['Oldham West and Royton', 'Lab/Co-op'], 'Tyrie': ['Chichester', 'Con'], 'Gibb': ['Bognor Regis and Littlehampton', 'Con'], 'Grieve': ['Beaconsfield', 'Con'], 'Thompson': ['Midlothian', 'SNP'],
      # from 2010ed
      'Hoban': ['Fareham', 'Con'], 'Kirkbride': ['Bromsgrove', 'Con'], 'Syms': ['Poole', 'Con'], 'Hogg': ['Sleaford and North Hykeham', 'Con'], 'Breed': ['South-East Cornwall', 'LD'], 'McLoughlin': ['West Derbyshire', 'Con']

  }

  globalList = [key for key in globalDict.keys()]

  bigQList = pickle.load(open( "../data/basic1992000data.p", "rb" ))

  for i in range(len(bigQList)):

    localDict = {}
    localList = []



    for qID in bigQList[i].keys():

      questionDict = bigQList[i][qID]

      genName = ''
      genCons = ''
      genPart = ''


      if questionDict["name"] != "META":

        # print(questionDict["name"])


        question = questionDict["question"]
        # print(question)

        # print(questionDict["name"])
        # question = questionDict["question"]
        # print('original question: ')
        # print(question)
        # print('\n')

        questionRE = re.search(r'^(.*?):\s*(.*)', question)
        if questionRE:
          questionPrefix = questionRE.group(1)
          questionProper = questionRE.group(2)
          if 'Prime Minister' in questionPrefix or 'Speaker' in questionPrefix or 'Member' in questionPrefix:
            pass
          elif len(questionPrefix) > 80:
            #special case where something is odd, need to find an alternative
            print('!!!special case')
            print(questionPrefix)
            pass
          elif re.search(r'\(', questionPrefix) == None:
            titleRE = re.search(r'^\s*(?:\w+\.)\s(.*)', questionPrefix)
            if titleRE:
              memIDer = titleRE.group(1)
              for term in localList:
                if memIDer in term:
                  genName = term
                  genCons = localDict[genName][0]
                  genPart = localDict[genName][1]
                  pass
                else:
                  lookup = questionPrefix.split()[-1]
                  cond = 0
                  for key in globalDict.keys():
                    if lookup in key:
                      lookup = key
                      genName = lookup
                      genCons = globalDict[lookup][0]
                      genPart = globalDict[lookup][1]
                      cond = 1
                      break
                  if cond == 0:
                    print(questionPrefix)
                  pass
            else:
              memIDer = questionPrefix.split()[-1]
              for term in localList:
                if memIDer in term:
                  genName = term
                  genCons = localDict[genName][0]
                  genPart = localDict[genName][1]
                  # print('genName: ' + genName + ' , genCons: ' + genCons + ' , genPart: ' + genPart)
                else:
                  lookup = questionPrefix.split()[-1]
                  for key in globalDict.keys():
                    if lookup in key:
                      lookup = key
                      genName = lookup
                      genCons = globalDict[lookup][0]
                      genPart = globalDict[lookup][1]
              pass
          else:
            genRE = re.sub(r'^(?:(?:Q|\d|\.|\[|\s)*\]\s*)*', '', questionPrefix)
            ConAndPartRE = re.search(r'^(?:\s*(\w(?:\w|\s|\.|-|\')+\w))\s*\((.*?)\)\s*\((.*?)\)', genRE)
            if ConAndPartRE:
              genName = ConAndPartRE.group(1)
              genCons = ConAndPartRE.group(2)
              genPart = ConAndPartRE.group(3)
              localList.append(genName)
              localDict[genName] = [genCons, genPart]
            else:
              onlyConRE = re.search(r'^(?:\s*(\w(?:\w|\s|\.|-|\')+\w))\s*\((.*?)\)', genRE)
              if onlyConRE:
                genName = onlyConRE.group(1)
                genCons = onlyConRE.group(2)
                genPart = 'Unknown'
                if 'The Leader' in genName:
                  genName = onlyConRE.group(2)
                  genCons = 'Unknown'
                # print('genName: ' + genName + ', genCons: ' + genCons)
                # pass
              else:
                if 'Tom Harris' in questionPrefix:
                  genName = 'Tom Harris'
                  genCons = 'Glasgow, Cathcart'
                  genPart = 'Lab'
                pass

          if genName != '':
            questionDict["memName"] = genName
            questionDict["memCons"] = genCons
            questionDict["memPart"] = genPart
          # print('genName: ' + genName + ' , genCons: ' + genCons + ' , genPart: ' + genPart)

          if genPart == 'Unknown':
            if 'Prime Minister' in questionPrefix or 'Speaker' in questionPrefix or 'Member' in questionPrefix:
              pass
            else:
              lookup = questionDict['name'].split()[-1]
              for key in localDict.keys():
                if lookup in key:
                  lookup = key
                  genName = lookup
                  genCons = localDict[lookup][0]
                  genPart = localDict[lookup][1]
              for key in globalDict.keys():
                if lookup in key:
                  lookup = key
                  genName = lookup
                  genCons = globalDict[lookup][0]
                  genPart = globalDict[lookup][1]


            if genName == '' or genPart == 'Unknown':
              if 'Prime Minister' in questionPrefix or 'Speaker' in questionPrefix or 'Member' in questionPrefix:
                pass
              else:
                ugh = ugh.union([questionDict['name']])
                lost +=1
                # print()
                # print(localDict)
                # print(questionDict["date"])
                # print(questionDict['raw'])

          if genName != '' and genPart != 'Unknown':
            counter += 1
            finalQs.append(questionDict)
        else:  # this triggers if we haven't found a separator. Only a couple of questions appear missed.
          # print(question)
          pass

        # print(questionDict)
  print('total good:' + str(counter))
  print(list(ugh))
  print('length of ugh list: ' + str(len(list(ugh))))
  print('lost: ' + str(lost))
          # print(questionPrefix)

          # print(questionPrefix)
          # print(questionProper)
        # else:
        #   # print('\n~~~~ New Question ~~~~\n')
        #   # print(questionDict["name"])
        #   # print('original question: ')
        #   # print(question)
        #   # print('\n')
        #   pass
    # input('x')

  return finalQs


def searchNames():

  # finally, a clever trick.
  # We pipe every name which isn't found from the main function into this function, which then
  # checks to see whether the data was somewhere else in the HTML files

  names = updateBasicData()

  outList = {}

  for file in os.listdir('../hansardBefore2010ed'):
    # file = 'vol416-cm200304-vo040107-40107-03_sbhd2.html'
    fileLoc = os.path.join(parentDir, 'hansardBefore2010ed/' + file)
    with codecs.open(fileLoc, "rb", encoding="utf-8", errors='ignore') as f:

      for line in f:

        for name in names:
          if re.search(name.split()[-1], line):
            # print(line)
            ConAndPartRE = re.search(r'\((.*?)\)\s*\((.*?)\)', line)
            if ConAndPartRE:
              genCons = ConAndPartRE.group(1)
              genPart = ConAndPartRE.group(2)
              genName = name.split()[-1]
              outList[genName] = [genCons, genPart]
  print(outList)


theseQs = updateBasicData()

funCount = 0

major1 = ['Con']
majorcas = ['UUP']
blair = ['Lab', 'Lab/Co-op', 'Lab/ Co-op']
brown1 = ['Lab', 'Lab/Co-op', 'Lab/ Co-op']
camclegg = ['Con', 'LD']
cam2 = ['Con']
may1 = ['Con']
may2 = ['Con']
may2cas = ['DUP']

def findAffi(party, date):
  gov = []
  cas = []
  # Determine the government
  if date <= 19961207:
    gov = major1
  elif date <= 19970502:
    gov = major1
    cas = majorcas
  elif date <= 20070627:
    gov = blair
  if date <= 20100511:
    gov = brown1
  elif date <= 20150508:
    gov = camclegg
  elif date <= 20160713:
    gov = cam2
  elif date <= 20170611:
    gov = may1
  else:
    gov = may2
    cas = may2cas
  # Is this part in government?
  if party in gov:
    return 'gov'
  elif party in cas:
    return 'cas'
  else:
    return 'opp'

allParties = set([])

govCount = 0
oppCount = 0

finalQs = []
print("go!")
print()
print("hoi")

for q in theseQs:
  # print(q)
  if q["question"] and q["memPart"] and q["date"]:
    if ':' in q["question"]:
      que = q["question"][q["question"].find(":")+1:].strip()
    else:
      que = q["question"].strip()
    affi = findAffi(q["memPart"], int(q["date"]))
    finalQs.append({"Question":que, "memName":q["memName"],  "memCons":q["memCons"], "memPart":q["memPart"], "date":q["date"], "memAffi":affi})
    allParties.add(q["memPart"])
    funCount += 1


def d_dict_to_csv(dic):
  keys = dic[0].keys()
  print(keys)
  with open('../data/qbankextra.csv', 'w', newline='',encoding='utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(dic)
  return

d_dict_to_csv(finalQs)

print(len(finalQs))
print(allParties)

# searchNames()

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
# getQuestion()
# cleanup()
# removeColumns()
