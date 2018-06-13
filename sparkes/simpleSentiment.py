# a very rough and tumble approach to sentiment analysis, with very inefficient scripts to count the number of 'sentiment' words, using prebuilt dictionaries.

# lexicons from https://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html#lexicon

import csv

posWords = []
negWords = []


def loadFBS(file, list):

  with open('../additionalData/opinion-lexicon-English/' + file +'.txt', encoding='latin-1') as f:
    for line in f:
      if line[0] == ';':
        pass
      else:
        if len(line) > 1:
          list.append(line[:-1])



loadFBS('positive-words', posWords)
loadFBS('negative-words', negWords)

def countQSentiment():

  qCounts = []
  qCount = 0

  qCountPosTotal = 0
  qCountNegTotal = 0
  qLength = 0


  with open('../data/combinedQBank.csv', encoding='utf-8') as f:
    reader = list(csv.DictReader(f))
    # print(reader)
    for q in reader:
      posCount = 0
      negCount = 0
      question = q['Question']
      question = question.split()
      for word in question:
        if len(question) < 350:
          qLength += 1
        if word in posWords:
          posCount += 1
          qCountPosTotal += 1
        if word in negWords:
          negCount += 1
          qCountNegTotal += 1
      qCounts.append([posCount, negCount])
      qCount += 1
      # print(qCount)

  qCountPosAv = qCountPosTotal/qCount
  qCountNegAv = qCountNegTotal/qCount
  qLengthAv = qLength/qCount

  # print(qCounts)

  print(qCountPosAv)
  print(qCountNegAv)
  print(qLengthAv)


def countMRSentiment():

  mCounts = []
  mCount = 0

  mCountPosTotal = 0
  mCountNegTotal = 0
  mLength = 0


  with open('../additionalData/sstSentences/datasetSentences.txt', encoding='utf-8') as f:
    for line in f:
      review = line[5:-1]
      review = review.split()

      posCount = 0
      negCount = 0

      for word in review:
        mLength += 1
        if word in posWords:
          posCount += 1
          mCountPosTotal += 1
        if word in negWords:
          negCount += 1
          mCountNegTotal += 1
      mCounts.append([posCount, negCount])
      mCount += 1
      # print(mCount)

  mCountPosAv = mCountPosTotal/mCount
  mCountNegAv = mCountNegTotal/mCount
  mLengthAv = mLength/mCount

  # print(mCounts)

  print(mCountPosAv)
  print(mCountNegAv)
  print(mLengthAv)

# countQSentiment()
# countMRSentiment()


def qLength():
  with open('../data/combinedQBank.csv', encoding='utf-8') as f:
      reader = list(csv.DictReader(f))
      # print(reader)
      for q in reader:
        question = q['Question']
        question = question.split()
        if len(question) > 300:
          # print(q)
          print(q['Question'])


def qWords():
  with open('../data/combinedQBankAnon.csv', encoding='utf-8') as f:
      reader = list(csv.DictReader(f))
      # print(reader)
      for q in reader:
        question = q['Question']
        question = question.split('.')
        for line in question:
          print(line)



qWords()
