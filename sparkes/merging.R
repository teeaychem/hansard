# Quick R script to combine the two different question banks

currentDir = dirname(rstudioapi::getActiveDocumentContext()$path)
setwd(currentDir)
getwd()

# a = read.csv("../data/qbank.csv")
# b = read.csv("../data/qbankextra.csv")

a = read.csv("../data/qbank.csv")
b = read.csv("../data/qbankextra.csv")


aQ = as.character(a$Question)
bQ = as.character(b$Question)
aName = as.character(a$memName)
bName = as.character(b$memName)
aCons = as.character(a$memCons)
bCons = as.character(b$memCons)
aPart = as.character(a$memPart)
bPart = as.character(b$memPart)
aDate = as.numeric(a$date)
bDate = as.numeric(b$date)
aAffi = as.character(a$memAffi)
bAffi = as.character(b$memAffi)



Question <- c(aQ, bQ)
memName <- c(aName, bName)
memCons <- c(aCons, bCons)
memPart <- c(aPart, bPart)
date <- c(aDate, bDate)
memAffi <- c(aAffi, bAffi)


combinedQBank <- data.frame(Question, memName, memCons, memPart, date, memAffi)

# write combined CSV
write.csv(combinedQBank, file = "../data/combinedQBank.csv")

# number of questions
nrow(combinedQBank)


