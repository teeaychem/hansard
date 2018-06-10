#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv

questions = []
with open('../data/combinedQBankAnon.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for q in reader:
        questions.append([q['Question'], q['memAffi']])


# lower the questions to make things easier
for question in questions:
  question[0] = question[0].lower()

def testWord(word):
  gov = 0
  opp = 0
  # resetCounters()
  for question in questions:
    if word in question[0].split():
      if question[1] == 'gov':
        gov = gov + 1
      else:
        opp = opp + 1
  if (gov == 0 and opp == 0):
    print(word)
  return [word, gov, opp, gov/(gov+opp), opp/(gov+opp), (gov+opp)/len(questions)]


def readTest(testresult):
  print('results for: ' + testresult[0])
  print('\tgov: ' + str(testresult[1]))
  print('\topp: ' + str(testresult[2]))
  print('\tpercentage gov: ' + str(testresult[3]))
  print('\tpercentage opp: ' + str(testresult[4]))
  print('\tpercentage all: ' + str(testresult[5]))

def testString(testresult):
  string =  ('results for: ' + testresult[0]) + '\n' + \
  ('\tgov: ' + str(testresult[1])) + '\n' + \
  ('\topp: ' + str(testresult[2])) + '\n' + \
  ('\tpercentage gov: ' + str(testresult[3])) + '\n' + \
  ('\tpercentage opp: ' + str(testresult[4])) + '\n' + \
  ('\tpercentage all: ' + str(testresult[5]))
  return string


wordList = set([])

for data in questions:
  question = set(data[0].split())
  wordList = wordList.union(question)

wordList = list(wordList)

worryWords = []

for word in wordList:
  limit = 20
  result = testWord(word.lower())
  allPerc = .3
  partPerc = .6
  if result[5] > allPerc:
    if (result[3] >= partPerc or result[4] >= partPerc):
      readTest(result)
      worryWords.append(result)

# thefile = open('wordAnalysis.txt', 'w')
# for result in worryWords:
#   thefile.write("%s\n" % testString(result))


# import spacy
# nlp = spacy.load('en_core_web_sm')
# doc = nlp(questions[32][0])
# print([(w.text, w.pos_) for w in doc])

# from sklearn.model_selection import train_test_split
# import pandas as pd

# questions = []
# with open('../sparkes/altqbank.csv', encoding='utf-8') as f:
#   reader = csv.DictReader(f)
#   for q in reader:
#     questions.append([q['Question'], q['memAffi']])

# print('loading csv')
# questions = pd.read_csv('../sparkes/altqbank.csv')
# print('finished loading csv')
