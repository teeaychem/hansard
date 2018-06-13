# functions to get sentences from question bank
# Not very effective when the data has no been 'anonymised', as hon. … etc. causes problems


import csv
import re


sList = []

directory = '../notebooks/data/'
inputFile = 'anon_test_data'
outputFile = inputFile + 'Sentences'

def readSentences():
   with open(directory + inputFile + '.csv', encoding='utf-8') as f:
      reader = list(csv.reader(f))
      for q in reader:
        # print(q)
        if 'memAffi' in q:
          memAffi = q['memAffi']
        else:
          memAffi = q[1]
        if 'Question' in q:
          question = q['Question']
        else:
          question = q[0]
        question = re.split('(?<=[a-z][\.?!:])\s+(?=[A-Z])', question)
        for line in question:
          sentence = line.strip()
          sList.append({'Question' : sentence, 'memAffi' : memAffi })


def d_dict_to_csv(dic):
  keys = dic[0].keys()
  print(keys)
  with open(directory + outputFile + '.csv', 'w', newline='',encoding='utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(dic)
  return


readSentences()
d_dict_to_csv(sList)


# print(sList)