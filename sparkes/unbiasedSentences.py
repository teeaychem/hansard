# functions to get sentences from question bank
# Not very effective when the data has no been 'anonymised', as hon. … etc. causes problems


import csv
import re
import random

sList = []
newSList = []

directory = '../notebooks/data/'
inputFile = 'anon_train_dataSentences'
outputFile = inputFile + 'Unbiased'

govCount = 0
oppCount = 0

def readSentences():

  govCount = 0
  oppCount = 0
  newGovCount = 0
  newOppCount = 0
  maxCount = 0

  with open(directory + inputFile + '.csv', encoding='utf-8') as f:
    reader = list(csv.reader(f))[1:]
    reader = random.sample(reader, len(reader))

    for q in reader:
      memAffi = q[1]
      question = q[0]
      if memAffi == 'gov':
        govCount += 1
      else:
        oppCount += 1
    maxCount = min(govCount, oppCount)

    print(maxCount)

    for q in reader:

      if newGovCount == maxCount and newOppCount == maxCount:
        break
      else:
        memAffi = q[1]
        question = q[0]

        if memAffi == 'gov':
          if newGovCount < maxCount:
            newGovCount += 1
            newSList.append({'Question' : question, 'memAffi' : memAffi })
          else:
            pass
        else:
          if newOppCount < maxCount:
            newOppCount += 1
            newSList.append({'Question' : question, 'memAffi' : memAffi })
          else:
            pass



        # question = re.split('(?<=[a-z][\.?!:])\s+(?=[A-Z])', question)
        # for line in question:
        #   sentence = line.strip()
        #   sList.append({'Question' : sentence, 'memAffi' : memAffi })

  print('oldGov: ' + str(govCount))
  print('oldOpp: ' + str(oppCount))
  print('newGov: ' + str(newGovCount))
  print('newOpp: ' + str(newOppCount))


def d_dict_to_csv(dic):
  keys = dic[0].keys()
  print(keys)
  with open(directory + outputFile + '.csv', 'w', newline='',encoding='utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(dic)
  return


readSentences()
d_dict_to_csv(newSList)


# print(sList)