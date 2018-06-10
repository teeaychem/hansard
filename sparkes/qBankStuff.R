currentDir = dirname(rstudioapi::getActiveDocumentContext()$path)
setwd(currentDir)
getwd()

a = read.csv("../data/combinedQBank.csv")


summary(a$memAffi)


a$Question[3]


